# Contributing to yaml2pptx

Thanks for your interest in contributing!

## Getting Started

```bash
git clone https://github.com/fredrsat/yaml2pptx.git
cd yaml2pptx
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
pytest --cov=yaml2pptx          # With coverage
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check src/
ruff format src/
```

## Pull Requests

1. Fork the repo and create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run `pytest` and `ruff check` to verify
5. Submit a PR with a clear description of the change

## Adding a Slide Type

To add a new slide type:

1. Create a renderer in `src/yaml2pptx/components/` (see existing types for patterns)
2. Register it in `src/yaml2pptx/components/renderer.py`
3. Add a snippet in `vscode-extension/snippets/yaml2pptx.json`
4. Add the type to `vscode-extension/schemas/yaml2pptx.schema.json`
5. Add a section to `README.md`
6. Add an example slide to `examples/showcase.yaml`

## Adding a Theme

To add a new theme:

1. Add the theme definition in `src/yaml2pptx/themes.py`
2. Add corresponding colors to `vscode-extension/media/preview.js`
3. Create an example presentation in `examples/`
4. Add the theme to the README themes table

## Reporting Issues

Open an issue at [github.com/fredrsat/yaml2pptx/issues](https://github.com/fredrsat/yaml2pptx/issues) with:
- What you expected
- What happened
- Your YAML file (or a minimal reproduction)
- Python version and OS
