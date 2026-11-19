"""Tecplot style macros: list the shipped styles, copy them into a folder to play.

Each style is one macro file in style_macros/, named after the style: the style
line-half is line-half.mcr. The folder is the registry, so a new .mcr there is a new
style. Its first comment line after the #!MC header is the description that
`lab tecplot styles` lists; keep it to one line.

A style sets only what every figure of its kind shares (frame size, fonts, grid
lines, legend). What belongs to one plot (axis titles, ranges, spacing, contour
levels) stays in that plot's layout, so a style can be played on a finished layout
without undoing its settings.
"""

# --------------------------------------------------
# import necessary modules
# --------------------------------------------------
from __future__ import annotations

from collections.abc import Sequence
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

# --------------------------------------------------
# constants
# --------------------------------------------------
# folder of the shipped macros, inside this package
STYLE_FOLDER = "style_macros"
STYLE_SUFFIX = ".mcr"


# --------------------------------------------------
# public API
# --------------------------------------------------
def list_styles() -> dict[str, str]:
    """The shipped styles and their one-line descriptions.

    Returns:
        Style name (e.g. "line-half") to description, sorted by name.
    """

    # read each macro's description
    styles = {}
    for name, macro_file in _style_files().items():
        styles[name] = _description(macro_file)

    return styles


def write_styles(names: Sequence[str], output_dir: Path, force: bool = False) -> list[Path]:
    """Copy style macros into a folder, to play in Tecplot.

    Nothing is written unless every name is a shipped style and, without force,
    no target file exists yet.

    Args:
        names: Style names, e.g. ["line-half", "contour-full"]; repeats count once.
        output_dir: Folder to write into (created if missing).
        force: Overwrite macro files that already exist.

    Returns:
        The written files, in the order of names.

    Raises:
        ValueError: If no name is given or a name is not a shipped style.
        FileExistsError: If a target file exists and force is not set.
    """

    # validate inputs: at least one name, every name a shipped style
    macro_files = _style_files()
    if not names:
        raise ValueError("no style given; choose from: " + ", ".join(macro_files))
    unknown = [name for name in names if name not in macro_files]
    if unknown:
        raise ValueError(
            f"unknown style {', '.join(unknown)}; choose from: {', '.join(macro_files)}"
        )

    # the files to write, one per style (dict.fromkeys drops repeats, keeps the order)
    unique_names = list(dict.fromkeys(names))
    targets = {}
    for name in unique_names:
        targets[name] = output_dir / f"{name}{STYLE_SUFFIX}"

    # check: never overwrite without force, and write nothing if one file is in the way
    existing = [str(target) for target in targets.values() if target.exists()]
    if existing and not force:
        raise FileExistsError(f"already exists: {', '.join(existing)}; use --force to overwrite")

    # write byte-for-byte copies of the shipped macros
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, target in targets.items():
        target.write_bytes(macro_files[name].read_bytes())

    written = list(targets.values())

    return written


# --------------------------------------------------
# helpers
# --------------------------------------------------
def _style_files() -> dict[str, Traversable]:
    """The shipped macro files by style name, sorted by name."""

    # list the package folder (works for an installed wheel as well as a checkout)
    folder = resources.files("lab_env.tecplot") / STYLE_FOLDER
    macro_files = {}
    for entry in folder.iterdir():
        if entry.name.endswith(STYLE_SUFFIX):
            name = entry.name.removesuffix(STYLE_SUFFIX)
            macro_files[name] = entry

    # sort by name, so listings and error messages are stable
    sorted_files = dict(sorted(macro_files.items()))

    return sorted_files


def _description(macro_file: Traversable) -> str:
    """A macro's first comment line after its #!MC header, without the leading '#'."""

    # find the first comment line that isn't the header
    description = ""
    for line in macro_file.read_text(encoding="utf-8").splitlines():
        is_header = line.startswith("#!MC")
        if line.startswith("#") and not is_header:
            description = line.removeprefix("#").strip()
            break

    return description
