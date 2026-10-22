# Repository layout

```
PROTOCOL.md          labelling protocol: landmark definitions, grades, examples
CHANGES.md           one entry per work package: built, left, open questions
docs/                criteria, data, related work, this file
data/manifests/      image IDs per split with source, metadata and hash; no images
data/labels/         keypoints and grades exported from Label Studio
src/cxrqa/io/        DICOM and PNG loading, pixel spacing, CheXmask, sampling, overlays
src/cxrqa/landmarks/ keypoint model, rib segmentation, contour readers
src/cxrqa/metrics/   collimation, rotation, inspiration, scapula: landmarks in, number out
src/cxrqa/grading/   threshold learning (ROC, Youden), grades with reason strings
src/cxrqa/report/    overlay PNG, JSON, DICOM Structured Report
service/             FastAPI app and Orthanc plugin script
ui/                  TypeScript review viewer
eval/                agreement statistics, accuracy, figures
notebooks/           exploration only, never imported
tests/               integration tests on a synthetic data directory; `data`-marked tests on real downloads
```

## Rules

- Metric functions are pure and cite their source paper in the docstring.
- Every grade carries a reason string a radiographer can read.
- Thresholds live in `grading/thresholds.yaml`, learned from labels, never hard-coded.
- Patient-level splits; `data/manifests/test.csv` is never used for training or tuning.
- No image, DICOM or model weight file is committed; pre-commit refuses them.
- Tooling: uv, ruff, mypy strict, pytest, pre-commit, GitHub Actions on Python 3.11 and 3.12.
