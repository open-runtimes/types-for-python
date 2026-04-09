# Publishing

This package is published to [PyPI](https://pypi.org/project/open-runtimes/).

## Setup

1. Create a PyPI account at https://pypi.org
2. Generate an API token at https://pypi.org/manage/account/token/
   - Scope it to the `open-runtimes` project (or all projects for the first upload)
3. Add the token as a GitHub Actions secret:
   - Secret name: `PYPI_API_TOKEN`
   - Secret value: the generated token (starts with `pypi-`)

## Publishing

Publishing is automated via GitHub Actions. To publish a new version:

1. Create a new GitHub release with a tag matching the desired version (e.g., `0.1.0`)
2. The workflow will automatically update `pyproject.toml` and publish to PyPI

## Manual Publishing

```bash
pip install build twine
python -m build
twine upload dist/*
```
