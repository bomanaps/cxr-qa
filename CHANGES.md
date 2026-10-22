# Changes

## WP1: data pipeline (complete, branch `wp1-data-pipeline`, 2026-10-22)

Built: `cxrqa.io.nih` (metadata loader, adult PA/AP filter, per-image per-axis PNG pixel
spacing derived from the original acquisition geometry), `cxrqa.io.chexmask` (streaming
reader, RLE decode and encode matching the authors' code, landmark split 44/50/26),
`cxrqa.io.image` (grayscale load, SHA-256), `cxrqa.io.sample` (adult PA with Dice RCA
mean of at least 0.7, one image per patient, stratified by age band and Dice tertile,
manifest with hashes), `cxrqa.io.overlay` (contours drawn on images). Integration tests:
a synthetic data directory (NIH CSV, PNGs, CheXmask CSV generated from the same polygons)
drives the sampler and overlay CLIs end to end; two `data`-marked tests check real downloads.

Also: README reduced to install, run and links; details moved to `docs/criteria.md`,
`docs/data.md`, `docs/layout.md`. `PROTOCOL.md` v0.2 drafted with every rule cited and
open points marked REVIEW for a radiographer.

Verified on real metadata: 112,120 rows, 30,805 patients, 67,310 PA / 44,810 AP; 64,582
adult PA. Original pixel spacing takes 12 distinct values from 0.115 to 0.1988 mm; original
widths 1,143 to 3,827 px; so a single PNG spacing would be wrong by up to a factor of 3.

Acceptance: all 112,120 NIH PNGs downloaded (42 GB, SHA-256 of each archive recorded) and
the 2.19 GB CheXmask ChestX-Ray8.csv validated row by row (see `docs/data.md`).
`python -m cxrqa.io.sample --n 2000` wrote `data/manifests/nih_pa_sample.csv`: 2,000 adult
PA images, 2,000 distinct patients, Dice RCA mean of at least 0.705, nine strata, SHA-256
per file, per-axis spacing 0.30 to 0.42 mm. Twenty overlays inspected; contours follow the
lung fields, including an image with a pacemaker and one with visible collimation borders.

Left: nothing. Open questions: none new.

## WP0: repository and tooling (2026-10-21)

Built: `src` layout with the five subpackages, `pyproject.toml` (uv, hatchling, ruff, mypy
strict, pytest), pre-commit hooks that refuse image and DICOM files, GitHub Actions CI on
Python 3.11 and 3.12, `.env.example` describing the expected `DATA_DIR` layout, `README.md`,
`PROTOCOL.md` skeleton with the EUR 16260 PA criteria quoted verbatim and the rotation sign
convention fixed, `docs/related-work.md`.

Left: `docker-compose.yml` (WP7), all code.

Open questions: whether BIMCV permits publishing labels keyed to PadChest image IDs; whether
the von Berg 2024 annotations or the ChestX-rayQuality labels will be released.
