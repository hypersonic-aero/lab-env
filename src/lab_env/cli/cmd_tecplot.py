"""Tecplot command group."""

# --------------------------------------------------
# import necessary modules
# --------------------------------------------------
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from lab_env.tecplot import export_layouts, list_styles, write_styles
from lab_env.tecplot.export import DEFAULT_FORMAT, DEFAULT_WIDTH

# --------------------------------------------------
# Tecplot command group
# --------------------------------------------------
tecplot_app = typer.Typer(
    help="Run portable Tecplot command wrappers.",
    no_args_is_help=True,
)


# --------------------------------------------------
# export command
# --------------------------------------------------
@tecplot_app.command("export")
def cmd_tecplot_export(
    layouts: Annotated[
        list[Path],
        typer.Argument(help="Tecplot .lay or .lpk files to export."),
    ],
    output_format: Annotated[
        str,
        typer.Option("--format", "-f", help="Tecplot image format."),
    ] = DEFAULT_FORMAT,
    width: Annotated[
        int,
        typer.Option("--width", "-w", min=1, help="Image width in pixels."),
    ] = DEFAULT_WIDTH,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Common output directory."),
    ] = None,
    tecplot_executable: Annotated[
        Path | None,
        typer.Option("--tecplot", help="Tecplot executable path."),
    ] = None,
) -> None:
    """Export Tecplot layouts to image files."""

    try:
        files = export_layouts(
            layouts,
            output_format=output_format,
            width=width,
            output_dir=output_dir,
            tecplot_executable=tecplot_executable,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1) from exc

    typer.echo(f"wrote {len(files)} file(s)")
    for file_path in files:
        typer.echo(file_path)


# --------------------------------------------------
# styles command
# --------------------------------------------------
@tecplot_app.command("styles")
def cmd_tecplot_styles(
    names: Annotated[
        list[str] | None,
        typer.Argument(help="Styles to write, e.g. line-half; none: list the styles."),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", help="Folder to write the macros into."),
    ] = Path("."),
    force: Annotated[
        bool,
        typer.Option("--force", help="Overwrite macro files that already exist."),
    ] = False,
) -> None:
    """List the Tecplot style macros, or write the named ones to play in Tecplot."""

    # no names: list the styles, name and description in two columns
    if not names:
        styles = list_styles()
        name_width = max(len(name) for name in styles)
        for name, description in styles.items():
            typer.echo(f"{name:<{name_width}}  {description}")
        typer.echo("")
        typer.echo("Write one: lab tecplot styles NAME..., then play it in Tecplot")
        typer.echo("(Scripting > Play Macro/Script) and save the layout.")
        return

    # write the named styles (nothing is written if one fails)
    try:
        files = write_styles(names, output_dir, force=force)
    except (OSError, ValueError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1) from exc

    # report, and how to use them
    for file_path in files:
        typer.echo(f"wrote {file_path}")
    typer.echo("Play in Tecplot with the frame active: Scripting > Play Macro/Script;")
    typer.echo("then save the layout, which keeps the style.")
