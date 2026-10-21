# Changes

## WP0: repository and tooling (2026-10-21)

Built: `src` layout with the five subpackages, `pyproject.toml` (uv, hatchling, ruff, mypy
strict, pytest), pre-commit hooks that refuse image and DICOM files, GitHub Actions CI on
Python 3.11 and 3.12, `.env.example` describing the expected `DATA_DIR` layout, `README.md`,
`PROTOCOL.md` skeleton with the EUR 16260 PA criteria quoted verbatim and the rotation sign
convention fixed, `docs/related-work.md`.

Left: `docker-compose.yml` (WP7), all code.

Open questions: whether BIMCV permits publishing labels keyed to PadChest image IDs; whether
the von Berg 2024 annotations or the ChestX-rayQuality labels will be released.
