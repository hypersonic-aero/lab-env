# Command Reference

## Global Options

`lab --config PATH COMMAND` selects a personal configuration file.
`lab --version` prints the installed version.

## `lab init`

Creates the selected configuration and parent directories. Existing files are
preserved and produce a nonzero exit code. No dotfiles are modified.

## `lab hosts`

Validates configuration and lists built-in and user-configured host names, SSH
destinations, and optional descriptions. It does not connect to a host.

## `lab doctor`

Validates configuration, reports whether the active shell is Bash or Zsh, checks
for a supported Conda initialization script, and locates `ssh`, `rsync`, `scp`,
and `sftp` on `PATH`. Missing clients or an enabled Conda integration without
`conda.sh` are warnings; invalid or missing configuration is an error.

## `lab connect HOST [REMOTE_ARGS]...`

Opens SSH to a built-in or user-configured host. Additional arguments run a remote command. Use
`--dry-run` to print the safely quoted command without starting a process. Use
`--` before remote arguments that begin with a hyphen.

## `lab pull HOST REMOTE_PATH [LOCAL_PATH]`

Pulls files with resumable rsync. The local path defaults to the current
directory. Archive mode, compression, partial files, append verification, and an
aggregate progress display are enabled. Transfers use `transfer_destination` if
configured, otherwise the host's SSH destination. Use `--dry-run` to preview the
command.

## `lab push HOST LOCAL_PATH REMOTE_PATH`

Pushes files with the same resumable rsync settings and destination selection as
`pull`. Local `~` paths are expanded without changing trailing-slash semantics.
Use `--dry-run` to preview the command.

## `lab tecplot export LAYOUT...`

Exports one or more Tecplot `.lay` or `.lpk` files through Tecplot's batch
interface. The default output is PNG with a width of 2000 pixels. Use
`--format`, `--width`, and `--output-dir` to override those defaults. Tecplot is
located from `--tecplot`, `TECPLOT_EXE`, `tec360` on `PATH`, or a standard
macOS application path, in that order.

The managed Bash/Zsh function `lay2pic` delegates to this command, so the
common case remains:

```bash
lay2pic figure.lay
lay2pic first.lay second.lay --width 3000
```

## `lab tecplot styles [NAME...]`

Without names, lists the Tecplot style macros that ship with lab-env, one line
each. With names, writes `NAME.mcr` for each into the current folder (or
`--output-dir`), ready to play in Tecplot with Scripting > Play Macro/Script.
Nothing is written if a name is unknown or a file already exists; `--force`
overwrites.

```bash
lab tecplot styles                         # list the styles
lab tecplot styles line-half contour-full  # write line-half.mcr, contour-full.mcr
```

| Style | Sets |
|---|---|
| `line-half`, `line-full` | XY line plot frame 3.25 x 2 in or 6.5 x 1.25 in, no border; Times titles (12 pt) and tick labels (10 pt); grid lines; legend in a white box |
| `contour-half`, `contour-full` | 2D plot frame 3.25 x 2 in or 6.5 x 1.5 in, no border; independent x and y scales; Times fonts as above; grid lines; contour legend in a box at the top right |
| `user-colors` | Custom colours `CUSTOM1` to `CUSTOM56`: eight ramps of seven shades |

A style sets only what every figure of its kind shares. Axis titles, ranges,
tick spacing and contour levels belong to each plot: set them in Tecplot. Play
the style once, then save the layout, which keeps it. One minor tick between
major ticks takes effect once a plot's tick spacing is set; while it is
automatic, Tecplot picks the minor ticks itself.

## `lab shell preview`

Prints the detected shell, startup paths, generated aliases and static state, and
managed blocks without writing files. Bash previews include `~/.bashrc` and the
login profile selected from `~/.bash_profile`, `~/.bash_login`, or `~/.profile`.
Use `--shell bash|zsh` and `--rc PATH` to override detection for inspection or
controlled tests.

## `lab shell install`

Validates personal configuration, writes generated shell setup to a static
fragment under `~/.config/lab-env/shell/`, and adds marked startup blocks.
For Bash, it installs into `.bashrc` and ensures the effective login profile also
loads it, unless that profile already sources `.bashrc`. Existing startup files
are backed up beside the original. Repeated installation is idempotent, and
symlinked startup files are rejected.

## `lab shell status`

Reports whether the managed startup blocks and generated shell file are present.

## `lab shell uninstall`

Backs up modified startup files, removes only lab-env-managed blocks, and deletes
the generated fragment. Other dotfile content is preserved.