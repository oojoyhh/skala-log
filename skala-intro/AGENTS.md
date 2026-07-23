# Repository Guidelines

## Project Structure & Module Organization
This repository is intentionally small and currently contains:
- `index.html`: main landing page
- `newsletter.html`: secondary static page
- `hello_world.py`: simple Python 3.11 example script

Keep new source files at the repository root unless the project grows enough to justify subdirectories. Use clear, descriptive names such as `about.html` or `data_loader.py`.

## Build, Test, and Development Commands
There is no formal build system yet. Use these direct commands:
- `python3.11 hello_world.py`: runs the Python example and prints `Hello World`
- Open `index.html` or `newsletter.html` in a browser to preview static content

If you add tooling later, document it here and prefer simple, repeatable commands.

## Coding Style & Naming Conventions
- Python: follow PEP 8, use 4-space indentation, and prefer `snake_case` for functions and variables.
- HTML: use semantic tags, consistent 2- or 4-space indentation, and lowercase file names.
- Keep edits minimal and readable; avoid introducing frameworks unless needed.

## Testing Guidelines
No automated test framework is configured yet. If you add code with behavior, include tests alongside it and document how to run them.
- Suggested Python test naming: `test_*.py`
- Place future tests in a dedicated `tests/` directory

## Commit & Pull Request Guidelines
Recent commits use short, imperative summaries such as `Add Newsletter` and `Git Repo Generation`. Keep commit messages concise and action-oriented.

Pull requests should include:
- a short description of the change
- any manual verification steps
- screenshots for visible HTML updates
- links to related issues when applicable

## Agent-Specific Instructions
Before creating files, check whether they already exist. Do not overwrite user-authored content unless explicitly requested.
