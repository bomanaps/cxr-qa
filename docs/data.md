# Data

Images never enter the repository. Only image identifiers, file hashes and our own labels are
published, subject to each source's terms.

## Directory layout

Set `DATA_DIR` in `.env`. Expected contents:

```
$DATA_DIR/nih/Data_Entry_2017_v2020.csv
$DATA_DIR/nih/images/*.png
$DATA_DIR/chexmask/ChestX-Ray8.csv
$DATA_DIR/padchest/                      metadata CSV; images only when needed
```

## Datasets

| Dataset          | Content                                                                                      | Use                                   | Access                                            | Terms                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| NIH ChestX-ray14 | 112,120 PNGs, 1024 x 1024, 8-bit; 30,805 patients; 67,310 PA, 44,810 AP; 64,582 adult PA     | Primary PA set; AP set for WP9        | https://nihcc.app.box.com/v/ChestXray-NIHCC       | No restrictions; link the Box site, cite Wang et al. CVPR 2017, acknowledge NIH CC      |
| CheXmask v1.0.0  | 657,566 lung and heart masks and 120-point contours; ChestX-Ray8.csv is 2.0 GB                | Lung-field contours                   | https://physionet.org/content/chexmask-cxr-segmentation-data/1.0.0/ | CC BY 4.0. Code (CheXmask-Database, HybridGNet) is GPL-3.0 and is not vendored |
| PadChest         | 160,868 images; 96,010 PA; 14,355 AP-horizontal; 5,158 AP-vertical; 1 TB                     | European external test; AP            | BIMCV form; granted 21 Oct 2026                   | Research Use Agreement: no redistribution, no derivative works except models and code; derived-label release awaiting written answer |
| VinDr-CXR        | 18,000 DICOM PA, Vietnam                                                                     | DICOM external test                   | PhysioNet credentialed (CITI course, DUA, reference) | Research only                                                                           |
| VinDr-RibCXR     | 245 images, 20 ribs per image as polygons (JSON); subset of VinDr-CXR                        | Rib segmentation training             | Signed DUA to the authors; requested 21 Oct 2026  | Research only; no modification or redistribution                                        |
| JSRT             | 247 PA, 2048 x 2048, 0.175 mm/px, film-digitised                                             | Clavicle model with SCR               | Registration at db.jsrt.or.jp                     | Research                                                                                |
| SCR              | Lungs, heart, both clavicles on all 247 JSRT images, two observers                           | Clavicle masks                        | https://zenodo.org/records/7056076                | CC BY 4.0                                                                               |

## NIH image files

All 112,120 PNGs are 1024 x 1024. Most are single-channel 8-bit (`L`); a minority are stored
as four-channel `RGBA` with identical colour channels. `cxrqa.io.image.load_grayscale`
converts every file to a single 8-bit channel, so downstream code never sees the difference.

## NIH pixel spacing

The metadata CSV gives `OriginalImage[Width,Height]` and `OriginalImagePixelSpacing[x,y]` of
the acquisition. The PNGs are 1024 x 1024 resamples of originals that are neither square nor
1024 px (widths 1,143 to 3,827; spacing 0.115 to 0.1988 mm in twelve distinct values). The
PNG spacing is therefore

```
spacing_x_mm = original_spacing_x * original_width  / 1024
spacing_y_mm = original_spacing_y * original_height / 1024
```

computed per image and per axis in `cxrqa.io.nih.load_metadata`. The commonly quoted
0.143 mm is the original spacing of many images, not the PNG spacing.

## CheXmask format

Columns: `Image Index`, `Dice RCA (Mean)`, `Dice RCA (Max)`, `Landmarks`, `Left Lung`,
`Right Lung`, `Heart`, `Height`, `Width`. Landmarks are 240 comma-separated numbers forming
120 (x, y) points: 0–43 right lung, 44–93 left lung, 94–119 heart. Masks are run-length
encoded as space-separated `start length` pairs over the row-major flattened image with
1-based starts. The authors recommend `Dice RCA (Mean)` of at least 0.7; the sampler applies
that cut.

Verified on the full ChestX-Ray8.csv (21 Oct 2026 download): 112,120 rows, one per NIH
image, no duplicates, all 1024 x 1024, every landmark and RLE field parses; 106,938 rows
have Dice RCA (Mean) of at least 0.7 (median 0.85). In 4,038 rows (3.6%) at least one
landmark lies outside the image, by a median of 9 px and at most 146 px. These are contour
points of lung fields cut off by the collimation and are kept: they are exactly the cases
in which the collimation distance is negative.

## Sampling

`cxrqa.io.sample` selects adult (age 18 or over) PA images with an acceptable CheXmask,
keeps one image per patient, stratifies by age band (18–39, 40–59, 60+) and Dice RCA
tertile, and writes `data/manifests/nih_pa_sample.csv` with SHA-256 of each PNG. Splits
are by patient; the test split is fixed before any model training.
