"""Tecplot style macros: the shipped files, and `lab tecplot styles`."""

# --------------------------------------------------
# import necessary modules
# --------------------------------------------------
from __future__ import annotations

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from lab_env.cli import app
from lab_env.tecplot import list_styles

runner = CliRunner()

# the styles the package ships
SHIPPED_STYLES = ["contour-full", "contour-half", "line-full", "line-half", "user-colors"]


# --------------------------------------------------
# helpers
# --------------------------------------------------
def shipped_bytes(name: str) -> bytes:
    """The shipped macro file of a style, as bytes."""
    folder = resources.files("lab_env.tecplot") / "style_macros"
    return (folder / f"{name}.mcr").read_bytes()


# --------------------------------------------------
# the shipped macros
# --------------------------------------------------
def test_every_style_is_a_described_tecplot_macro() -> None:
    """Each style starts with the macro header and has a one-line description."""

    # read
    styles = list_styles()

    # check: the expected styles, each described
    assert list(styles) == SHIPPED_STYLES
    for name, description in styles.items():
        assert description, name
        text = shipped_bytes(name).decode("utf-8")
        assert text.startswith("#!MC 1410\n"), name


def test_every_macro_line_is_a_command_a_block_or_a_comment() -> None:
    """Outside comments, each top-level line is a $! command (a typo there would be
    skipped by Tecplot, not reported); indented lines continue a command's block."""

    for name in SHIPPED_STYLES:
        for line in shipped_bytes(name).decode("utf-8").splitlines():
            is_blank = not line.strip()
            is_comment = line.startswith("#")
            is_block = line.startswith(" ")
            is_command = line.startswith("$!")
            assert is_blank or is_comment or is_block or is_command, f"{name}: {line!r}"


# --------------------------------------------------
# lab tecplot styles
# --------------------------------------------------
def test_styles_without_names_lists_them() -> None:
    """No names: every style with its description."""

    # run
    result = runner.invoke(app, ["tecplot", "styles"])

    # check
    assert result.exit_code == 0, result.output
    for name, description in list_styles().items():
        assert name in result.output
        assert description in result.output


def test_styles_writes_the_named_macros(tmp_path: Path) -> None:
    """Named styles are written as exact copies, <name>.mcr in the output folder."""

    # run
    result = runner.invoke(
        app, ["tecplot", "styles", "line-half", "contour-full", "-o", str(tmp_path)]
    )

    # check
    assert result.exit_code == 0, result.output
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "contour-full.mcr",
        "line-half.mcr",
    ]
    assert (tmp_path / "line-half.mcr").read_bytes() == shipped_bytes("line-half")
    assert (tmp_path / "contour-full.mcr").read_bytes() == shipped_bytes("contour-full")


def test_styles_refuses_to_overwrite_and_writes_nothing(tmp_path: Path) -> None:
    """One existing file: refused with one error line, the other style isn't written
    either; --force overwrites."""

    # an existing macro of the user's
    existing = tmp_path / "line-half.mcr"
    existing.write_text("# mine\n", encoding="utf-8")

    # run without --force
    refused = runner.invoke(
        app, ["tecplot", "styles", "line-half", "line-full", "-o", str(tmp_path)]
    )

    # check: nothing changed
    assert refused.exit_code == 1
    assert "error: " in refused.output
    assert "use --force" in refused.output
    assert existing.read_text(encoding="utf-8") == "# mine\n"
    assert not (tmp_path / "line-full.mcr").exists()

    # run with --force
    forced = runner.invoke(
        app, ["tecplot", "styles", "line-half", "line-full", "-o", str(tmp_path), "--force"]
    )

    # check: both written
    assert forced.exit_code == 0, forced.output
    assert existing.read_bytes() == shipped_bytes("line-half")
    assert (tmp_path / "line-full.mcr").read_bytes() == shipped_bytes("line-full")


def test_styles_refuses_an_unknown_name(tmp_path: Path) -> None:
    """An unknown name fails with the list of styles, and nothing is written."""

    # run
    result = runner.invoke(
        app, ["tecplot", "styles", "line-half", "line-quarter", "-o", str(tmp_path)]
    )

    # check
    assert result.exit_code == 1
    assert "unknown style line-quarter" in result.output
    assert "line-half" in result.output
    assert list(tmp_path.iterdir()) == []
