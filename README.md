# cxr-qa

Open, explainable measurement of positioning quality in adult frontal chest radiographs.

**Not a medical device. Not for clinical decisions.** Research and quality-assurance use only.

## What it measures

Each criterion maps a sentence of the European Guidelines on Quality Criteria for Diagnostic
Radiographic Images (EUR 16260, 1996, chest PA) to a number computed from anatomical landmarks.

| Criterion   | EUR 16260 basis                                                        | Metric                                                                 |
| ----------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Collimation | 1.1.4 Reproduction of the whole rib cage above the diaphragm           | Distance in mm from lung-field extreme to image border, four sides     |
| Rotation    | 1.1.2 Spinous process central between the medial ends of the clavicles | α = (dR − dL) / (dR + dL), d = clavicle head to spinous-process line   |
| Inspiration | 1.1.1 Full inspiration, 10 posterior ribs above the diaphragm          | Posterior ribs above each hemidiaphragm; cmax = max(cL, cR)            |
| Scapulae    | 1.1.3 Medial border of the scapulae outside the lung fields            | Overlap of medial scapular border with lung field, per side            |

Metric definitions follow von Berg et al., IMAGING 16(1):41–49, 2024 (doi:10.1556/1647.2024.00187).
Thresholds are learned from labelled data, not fixed in advance.

Models find anatomy. Grades are plain geometry on that anatomy, so every result can be checked
against the overlay by eye.

## Status

Work package 0 (repository and tooling). No models, metrics or labels yet.
See `CHANGES.md` for progress and `PROTOCOL.md` for the labelling protocol.

## Layout

```
PROTOCOL.md          labelling protocol, criteria, examples
data/manifests/      image IDs per split with source and hash (no images)
data/labels/         keypoints and grades (JSON/CSV)
src/cxrqa/io/        DICOM/PNG loading, pixel spacing, normalisation
src/cxrqa/landmarks/ keypoint model, rib segmentation, CheXmask reader
src/cxrqa/metrics/   collimation, rotation, inspiration, scapula
src/cxrqa/grading/   threshold learning, grades with reason strings
src/cxrqa/report/    overlay PNG, JSON, DICOM SR
service/             FastAPI app and Orthanc plugin script
ui/                  TypeScript review viewer
eval/                agreement statistics, accuracy, figures
notebooks/           exploration only, never imported
tests/               unit tests on synthetic landmark sets
```

## Quickstart

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/bomanaps/cxr-qa.git
cd cxr-qa
uv sync --extra dev
uv run pre-commit install
uv run pytest
```

Datasets are never stored in the repository. Copy `.env.example` to `.env` and set `DATA_DIR`
to the directory holding the downloads described there.

## Data

| Dataset          | Use                              | Terms                                                        |
| ---------------- | -------------------------------- | ------------------------------------------------------------ |
| NIH ChestX-ray14 | Primary PA and AP images         | Open; cite Wang et al. CVPR 2017; acknowledge NIH CC         |
| CheXmask         | Lung and heart contours          | CC BY 4.0 (PhysioNet open access)                            |
| PadChest         | European site, external test     | BIMCV Research Use Agreement; images never redistributed     |
| VinDr-CXR        | DICOM site, external test        | PhysioNet credentialed; images never redistributed           |
| JSRT + SCR       | Clavicle masks                   | JSRT registration; SCR CC BY 4.0 (Zenodo 7056076)            |
| VinDr-RibCXR     | Rib segmentation training        | Data use agreement; images never redistributed               |

Only image identifiers, hashes and our own labels are published, subject to each source's terms.

## Licence

Code: Apache-2.0. Labels: CC BY 4.0 where the source dataset's terms allow.
