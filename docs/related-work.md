# Related work and open resources

Compiled 21 October 2026 from a search of GitHub, arXiv, Papers with Code, PhysioNet, Zenodo
and Hugging Face for open code, labels and datasets for chest radiograph positioning quality.
Every item was checked at its source on that date.

## 1. Positioning-quality methods

| Work | Venue | What it does | Code | Labels | Licence |
| --- | --- | --- | --- | --- | --- |
| von Berg et al. 2024, "What patient positioning in chest X-ray is still acceptable?" | IMAGING 16(1):41–49, doi:10.1556/1647.2024.00187 | Collimation (four borders), clavicle asymmetry α, ribs above diaphragm on 64,315 NIH PA images; 920 annotated; 7 readers; learned thresholds | No | No | Paper CC BY-NC 4.0 |
| von Berg et al. 2020, "Robust chest x-ray quality assessment using CNNs and atlas regularization" | Proc SPIE 11313, doi:10.1117/12.2549541 | 3 CNNs + 2 atlases detect lung borders, posterior ribs, diaphragm, clavicle heads, spinous processes | No | No | Closed |
| von Berg et al. 2020, ECR poster C-05625 | doi:10.26044/ecr2020/C-05625 | Defines α = (dL − dR)/(dL + dR) and four collimation distances; median landmark errors 2.5–3.0 mm | No | No | — |
| Poggenborg et al. 2021, real-time feedback | medRxiv doi:10.1101/2021.06.10.21258326 | Philips checker at the console; optimal images 31.4% → 40.8% | No | No | All rights reserved |
| Nousiainen et al. 2021 | Phys Med 83:138–145 | Six CNN classifiers for inclusion edges, rotation, inspiration; 2,589 PA images; rotation AUC 0.70–0.72 | No | No | Closed |
| Sorace et al. 2024 | Radiography 30(1):107–115 | CNN on 2,375 AP images; technique and inspiration classes | No | No | Closed |
| Borisov et al. 2025 | Int J CARS 20(9):1829–1833 | Seven networks on 69,000+ images; missed anatomy, rotation, brightness, projection, metadata | No | No | Closed |
| Wang et al. 2026 | BMC Med Imaging 26:214 | Cervical spine, scapula, costophrenic angle compliance; 2,363 PA + 1,300 AP | No | On request | CC BY |
| Hu et al. 2022, ChestX-rayQuality | IEEE TMI, doi:10.1109/TMI.2022.3149171 | 480 images with scapula-overlap, clavicle-unflatness, lung-field-loss, artifact labels | No | Promised, not found | — |
| Ma et al. 2025 | Eur Radiol, PMC13035635 | Scapula–lung overlap ratio, clavicle tilt; 3,300 private images | No | No | — |
| Sun et al. 2024 | BJR, PMC11417390 | Rotation from lung-width asymmetry; 800 public images with private spine masks | No | No | — |
| Meng et al. 2022 | Eur Radiol doi:10.1007/s00330-022-08771-x | Clavicle, rotation, scapula cascade; 1,025 private images | No | No | — |

## 2. Open code touching the same metrics

| Repository | What it provides | Licence | Assessment |
| --- | --- | --- | --- |
| github.com/Paritt/WYVERN | Desktop GUI: rotation from medial clavicle ends vs spinous process; inspiration from lung and 9th posterior rib segmentation | None stated | Unpublished, unlicensed, unvalidated; no collimation or scapula; no PACS |
| github.com/Paritt/DeepInspire | Training code for rib/lung U-Nets; dataset on Google Drive | "Research purposes" | Provenance and size of the dataset unknown |
| github.com/ntm8813/cxr-quality-scorer | Streamlit rotation, inspiration, coverage, exposure scorers from lung masks | None stated | Private weights and validation set; method undocumented |
| github.com/DIAGNijmegen/opencxr | Image sorting (PA/AP/lateral, 90/180/270°, inversion), lung and heart segmentation on PA | Apache-2.0 | Orientation, not positioning; useful PA/AP sorter |
| github.com/mlmed/torchxrayvision | Dataset loaders (NIH, PadChest, VinDr-CXR, CheXpert, MIMIC); DenseNet/ResNet encoders; PSPNet segmenting clavicles, scapulae, lungs, heart, spine, diaphragm | Apache-2.0 | No ribs; no loaders for JSRT, SCR, VinDr-RibCXR, CheXmask |
| github.com/ConstantinSeibold/ChestXRayAnatomySegmentation (CXAS / PAX-Ray++) | 157-class anatomy segmentation incl. ribs, clavicles, scapulae, vertebrae | Code CC BY-NC-SA 4.0; data CC BY-NC 4.0 | Non-commercial licence; comparison only |
| gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/autoqc | Dataset-curation QC: inversion, projection, orientation, pacemakers | MIT | Not positioning |
| github.com/ngaggion/CheXmask-Database, github.com/ngaggion/HybridGNet | Lung and heart contour generation | GPL-3.0 | Use as a separate tool; not vendored |

## 3. Datasets

| Dataset | Content | Access | Licence |
| --- | --- | --- | --- |
| NIH ChestX-ray14 | 112,120 PNGs, 30,805 patients, 67,310 PA / 44,810 AP; CSV with view, original size and spacing | Open | No restrictions; attribution required |
| CheXmask v1.0.0 (PhysioNet) | 657,566 lung and heart masks and landmarks across ChestX-ray8, CheXpert, MIMIC-CXR-JPG, PadChest, VinDr-CXR | Open | CC BY 4.0 |
| PadChest | 160,868 images; 96,010 PA, 14,355 AP-horizontal, 5,158 AP-vertical | Form; granted 21 Oct 2026 | Research Use Agreement; no redistribution; derived label release pending written answer |
| VinDr-CXR | 18,000 DICOM PA, Vietnam | PhysioNet credentialed (CITI + DUA) | Research only |
| VinDr-RibCXR | 245 images, 20 ribs each, polygon JSON | Signed DUA by email; requested 21 Oct 2026 | Research only; no modification or redistribution |
| JSRT | 247 PA, 2048×2048, 0.175 mm/px, film-digitised | Registration | Research |
| SCR | Lungs, heart, both clavicles on all 247 JSRT images, two observers | Zenodo 7056076 | CC BY 4.0 |
| INESC TEC Montgomery heart and clavicle masks | 138 images | rdm.inesctec.pt/dataset/nis-2023-004 | CC BY-SA |
| Chest ImaGenome | Anatomical bounding boxes on MIMIC-CXR | PhysioNet credentialed | Research |

No public dataset was found with spinous-process or hemidiaphragm landmarks, or with per-criterion
positioning grades across more than one source dataset.

## 4. Commercial and patent context

The three von Berg metrics ship as Philips Radiology Smart Assistant and are covered by
US 10,751,016 and US 12,217,419. cxr-qa re-implements the published definitions for research
and quality assurance; it does not claim the metric ideas as new.

## 5. Gap statement

No licensed, peer-reviewed, validated open implementation of the collimation, clavicle-rotation,
rib-count and scapula metrics exists; no open per-criterion reference labels span several public
datasets; and no open tool connects such measurements to a PACS.
