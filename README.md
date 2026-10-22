# cxr-qa

Open, explainable measurement of positioning quality in adult frontal chest radiographs:
collimation, rotation, inspiration and scapula position, graded against EUR 16260.

**Not a medical device. Not for clinical decisions.** Research and quality-assurance use only.

Models locate anatomy. Grades are geometry on that anatomy, checkable on the overlay by eye.
Thresholds are learned from labelled data, not fixed in advance.

## Install

Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/bomanaps/cxr-qa.git && cd cxr-qa
uv sync --extra dev
uv run pre-commit install
cp .env.example .env    # set DATA_DIR
```

## Run

```sh
uv run pytest                                   # integration tests on synthetic data
DATA_DIR=... uv run pytest -m data              # checks against real downloads
uv run python -m cxrqa.io.sample --n 2000       # stratified manifest of adult PA images
uv run python -m cxrqa.io.overlay --n 20 --out /tmp/overlays
```

## Documents

- [Criteria and metrics](docs/criteria.md): EUR 16260 wording, metric definitions, sign conventions.
- [Data](docs/data.md): datasets, access, licences, directory layout, pixel spacing.
- [Repository layout](docs/layout.md): what each package does.
- [Related work](docs/related-work.md): prior methods, open code and datasets, gap statement.
- [Labelling protocol](PROTOCOL.md).
- [Changes](CHANGES.md): per work package.

## Licence

Code Apache-2.0. Labels CC BY 4.0 where the source dataset's terms allow.
