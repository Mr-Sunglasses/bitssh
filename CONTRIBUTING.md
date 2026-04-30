<!-- omit in toc -->
# Contributing to bitssh

First off, thanks for taking the time to contribute!

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them.

> If you like the project but don't have time to contribute, you can still support it by:
> - Starring the project
> - Sharing it with others
> - Referring to it in your own projects

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Development Setup](#development-setup)
- [Using Make](#using-make)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by the
[bitssh Code of Conduct](https://github.com/Mr-Sunglasses/bitssh/blob/main/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.

## I Have a Question

Before asking a question, please:

1. Read the [documentation](https://github.com/Mr-Sunglasses/bitssh/blob/master/README.md)
2. Search existing [Issues](https://github.com/Mr-Sunglasses/bitssh/issues)
3. Search the internet for answers

If you still need help, [open an issue](https://github.com/Mr-Sunglasses/bitssh/issues/new) and provide as much context as possible, including your Python version, OS, and bitssh version.

## I Want To Contribute

> **Legal Notice:** When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content, and that the content you contribute may be provided under the project license.

### Reporting Bugs

#### Before Submitting a Bug Report

- Make sure you are using the latest version of bitssh
- Check if the issue is really a bug and not a misconfiguration (read the [documentation](https://github.com/Mr-Sunglasses/bitssh/blob/master/README.md))
- Check if the bug has already been reported in the [issue tracker](https://github.com/Mr-Sunglasses/bitssh/issues?q=label%3Abug)
- Make sure your `~/.ssh/config` file exists and is properly formatted
- Collect information about the bug:
  - The full stack trace / traceback
  - Your OS and terminal emulator
  - Python version (`python --version`)
  - bitssh version (`bitssh --version`)
  - A sanitized copy of your SSH config (remove sensitive info like hostnames, IPs, and keys)

#### How to Submit a Good Bug Report

Use the [Bug Report template](https://github.com/Mr-Sunglasses/bitssh/issues/new?template=bug.yml) and fill in all the required fields. Include reproduction steps and expected vs actual behavior.

### Suggesting Enhancements

Use the [Feature Request template](https://github.com/Mr-Sunglasses/bitssh/issues/new?template=feature.yml) to suggest new features or improvements.

Before submitting, make sure to:

- Check if the feature already exists in the latest version
- Search existing issues to avoid duplicates
- Consider whether the feature benefits most bitssh users

### Your First Code Contribution

#### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/bitssh.git
cd bitssh
```

#### 2. Set Up the Development Environment

```bash
make dev
```

This creates a virtual environment, installs bitssh in editable mode with dev dependencies, and sets up pre-commit hooks.

#### 3. Create a Branch

```bash
git checkout -b my-feature-branch
```

Use a descriptive branch name, e.g. `fix/ssh-config-parsing` or `feature/host-filtering`.

#### 4. Make Your Changes

Edit the source code in `src/bitssh/`. The main modules are:

| File | Purpose |
|---|---|
| `src/bitssh/__main__.py` | Entry point and CLI argument handling |
| `src/bitssh/cli.py` | CLI interface orchestration |
| `src/bitssh/ui.py` | Terminal UI (TUI) rendering |
| `src/bitssh/prompt.py` | User interaction / host selection |
| `src/bitssh/utils.py` | SSH config parsing and utility functions |
| `src/bitssh/argument_parser.py` | Argument parsing logic |

#### 5. Run Tests

```bash
make test
```

#### 6. Lint and Format

```bash
make format   # auto-format code
make lint     # check for lint errors
make check    # run both lint and test (full CI check)
```

#### 7. Commit and Push

```bash
git add .
git commit -m "feat: add host filtering in TUI"
git push origin my-feature-branch
```

#### 8. Open a Pull Request

Open a pull request against the `master` branch. Fill in the PR template completely.

## Development Setup

### Prerequisites

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- make

### Install Dependencies

```bash
make dev
```

Or manually:

```bash
uv venv
uv pip install -e ".[dev]"
uv run pre-commit install
```

### Running bitssh Locally

```bash
make run
# or
uv run bitssh
# or
python -m bitssh
```

Make sure you have a valid `~/.ssh/config` file. See the [README](https://github.com/Mr-Sunglasses/bitssh#troubleshooting) for troubleshooting.

## Using Make

The project includes a `Makefile` with convenient commands for common development tasks. Run `make help` to see all available commands.

| Command | Description |
|---|---|
| `make dev` | Full setup: create venv, install deps, set up pre-commit hooks |
| `make setup` | Create venv and install dev dependencies |
| `make install` | Install the package in editable mode |
| `make test` | Run the test suite with coverage |
| `make lint` | Run linters (ruff) |
| `make format` | Auto-format code (ruff format + ruff check --fix) |
| `make check` | Run lint + test (full CI check) |
| `make run` | Run bitssh CLI |
| `make build` | Build distribution packages |
| `make bumpver-patch` | Bump patch version (e.g. 3.7.0 → 3.7.1) |
| `make bumpver-minor` | Bump minor version (e.g. 3.7.0 → 3.8.0) |
| `make bumpver-major` | Bump major version (e.g. 3.7.0 → 4.0.0) |
| `make clean` | Remove build artifacts, caches, and venv |

## Styleguides

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Use `ruff` for linting and formatting (configured in `pyproject.toml`)
- Line length: 100 characters
- Target Python version: 3.10+

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description
```

Common types:

| Type | Use for |
|---|---|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation changes |
| `refactor` | Code restructuring |
| `test` | Adding or updating tests |
| `chore` | Build, CI, or tooling changes |

Examples:

- `feat(ui): add search filter for host list`
- `fix(utils): handle missing SSH config gracefully`
- `docs: update installation instructions`
- `test(cli): add tests for argument parsing`

### Version Bumping

This project uses [bumpver](https://github.com/mbarkhau/bumpver) for version management. The version is defined in a single place — `src/bitssh/_version.py` — and everything else reads from it:

| File | What it does |
|---|---|
| `src/bitssh/_version.py` | Single source of truth: `__version__ = "3.7.0"` |
| `pyproject.toml` → `[tool.setuptools.dynamic]` | Reads version from `_version.py` at build time |
| `pyproject.toml` → `[tool.bumpver]` | Tracks the current version for bumpver CLI |
| `src/bitssh/__init__.py` | Imports `__version__` from `_version.py`, overrides with `importlib.metadata` at runtime |

To bump the version, use one of these make commands:

```bash
make bumpver-patch   # 3.7.0 → 3.7.1
make bumpver-minor   # 3.7.0 → 3.8.0
make bumpver-major   # 3.7.0 → 4.0.0
```

Each command will:

1. Update `__version__` in `src/bitssh/_version.py`
2. Update `current_version` in `pyproject.toml` `[tool.bumpver]`
3. Create a git commit with the message `"Bump version {old} -> {new}"`
4. Create a git tag (e.g. `v3.7.1`)

> **Note:** bumpver does **not** push to remote by default (`push = false`). You need to `git push && git push --tags` manually when ready.
