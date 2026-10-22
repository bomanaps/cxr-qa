# Labelling protocol

Version 0.2, draft for radiographer review. Not yet piloted.

Every rule below is taken from a cited source. Rules the sources do not settle are marked
**[REVIEW]** and must be confirmed or changed by a qualified radiographer before the pilot.
Nothing in this document is the labelling lead's own judgement.

Sources, cited by short name:

- **EUR** European Guidelines on Quality Criteria for Diagnostic Radiographic Images, EUR 16260 EN, 1996, chest PA criteria.
- **vB24** von Berg J, Hergaarden KFM, et al. IMAGING 16(1):41–49, 2024. doi:10.1556/1647.2024.00187.
- **ECR20** von Berg J, et al. ECR 2020 poster C-05625. doi:10.26044/ecr2020/C-05625.
- **Nous21** Nousiainen K, et al. Phys Med 83:138–145, 2021. doi:10.1016/j.ejmp.2021.03.014.
- **Wang26** Wang YC, et al. BMC Med Imaging 26:214, 2026. doi:10.1186/s12880-026-02278-3.
- **RCR** Royal College of Radiologists, AuditLive, Adapted Anatomical Image Criteria for PA Chest Radiography, 2011, reviewed 2022.
- **RMC** Radiology Masterclass, Chest X-ray Quality tutorial (rotation, inspiration, penetration), radiologymasterclass.co.uk.

## 1. Scope

Adults (18 years and older), frontal chest radiographs. PA erect for versions 0.x to 1.x;
AP and portable images are covered by section 9 from WP9. Lateral, paediatric and
non-chest images are excluded.

## 2. Image conventions

1. Images are displayed in standard radiographic orientation: the patient's right on the
   viewer's left. All left and right terms for anatomy refer to the **patient's** side.
   Collimation sides refer to **image** sides and are named top, bottom, image-left,
   image-right.
2. Coordinates are pixel (x, y), origin at the top-left corner, x to the right, y downward,
   on the image at labelling resolution (1024 x 1024 for NIH PNGs).
3. Millimetre values use the per-image, per-axis pixel spacing in the manifest.
4. Window and level may be adjusted freely while labelling. Zoom is encouraged for point
   placement; points are placed at the highest zoom at which the structure is visible.

## 3. Criteria measured

| Criterion   | EUR wording                                                                                                   | What is labelled                         |
| ----------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Inspiration | 1.1.1 Performed at full inspiration (... ribs above the diaphragm — either 6 anteriorly or 10 posteriorly)    | Right hemidiaphragm dome; posterior rib count, each side |
| Rotation    | 1.1.2 Symmetrical reproduction of the thorax as shown by central position of the spinous process between the medial ends of the clavicles | Both medial clavicle ends; three spinous-process points |
| Scapulae    | 1.1.3 Medial border of the scapulae to be outside the lung fields                                             | Overlap yes/no, each side                |
| Collimation | 1.1.4 Reproduction of the whole rib cage above the diaphragm                                                  | Nothing by hand; computed from CheXmask lung contours |
| Exposure    | 1.1.7 Visualization of the retrocardiac lung and the mediastinum; 1.1.8 Visualization of the spine through the heart shadow | Adequate yes/no (label only in v1) |

## 4. Landmarks

### 4.1 Medial clavicle ends (two points: `clavicle_R`, `clavicle_L`)

Source: EUR 1.1.2 "medial ends of the clavicles"; vB24 and ECR20 "clavicle heads", distance
measured from each to the spinous-process line.

1. Place the point on the most medial visible point of the cortical outline of the clavicle,
   at the sternal end, where the clavicle meets the sternoclavicular joint.
2. The point lies on the bone margin, not in the joint space.
3. If the medial end is overlapped by the first rib or by the mediastinal shadow, follow the
   cortical outline of the clavicle medially to where it ends and place the point there.
4. If the end cannot be located because of overlying devices (ECG leads, lines) or because it
   lies outside the image, place the best estimate and tick `clavicle_uncertain` for that
   side. Rotation is not graded from images with either side uncertain.

**[REVIEW]** Rule 1: confirm "most medial point of the cortical outline" against the
convention used in the reviewer's department.

### 4.2 Spinous-process line (three points: `spine_1`, `spine_2`, `spine_3`)

Source: EUR 1.1.2 "central position of the spinous process"; vB24 "spinous process line";
the SPIE 2020 method detects spinous processes as landmarks. Nous21 phrases the rotation
rule as "the medial ends of the collarbones were symmetrical around the spine".

1. Spinous processes appear as a vertical row of small teardrop or oval densities in the
   midline of the vertebral bodies.
2. `spine_1`: centre of the spinous process at the level of the clavicle ends (the vertebra
   whose spinous process lies between the two clavicle points, usually T2 to T4).
3. `spine_2`: centre of the spinous process two vertebrae above `spine_1`, or the highest
   spinous process fully visible if fewer than two are visible above.
4. `spine_3`: centre of the spinous process two vertebrae below `spine_1`.
5. The spinous-process line is the least-squares line through the three points; the
   software fits it. Distances dR and dL are measured perpendicular to that line.
6. If spinous processes are not identifiable through the mediastinum, place the points on the
   midline of the vertebral bodies instead and tick `spine_uncertain`.

**[REVIEW]** Rules 2 to 4: two vertebrae above and below is chosen so that the line spans
the clavicle level; confirm or change the span.

### 4.3 Right hemidiaphragm dome (one point: `diaphragm_R`)

Source: vB24 counts "ribs above the diaphragm" per side; ECR20 detects "diaphragm".

1. Place the point at the highest point (apex) of the right hemidiaphragm outline, the
   boundary between lung and the dense subdiaphragmatic shadow.
2. If the dome is flattened, place the point at the midpoint of the flattest segment.
3. If the dome is obscured (effusion, consolidation, pacemaker), place the best estimate and
   tick `diaphragm_uncertain`.

The left dome is not placed in v1; the left rib count (5.1) is read directly.

### 4.4 Lung-field contours

Taken from CheXmask (Gaggion et al., Sci Data 2024), not labelled by hand. Images with
`Dice RCA (Mean)` below 0.7 are excluded by the sampler. The labeller records
`lung_contour_wrong = yes` when the overlaid contour visibly misses the lung field, and the
image is excluded from collimation grading.

## 5. Counts and choices

### 5.1 Posterior ribs above the hemidiaphragm (`ribs_R`, `ribs_L`, each 0 to 12 in steps of 0.5)

Source: EUR 1.1.1 "10 posteriorly"; Nous21 inspiration appropriate when "the posterior side
of the tenth rib [was] visible over the right lung"; vB24 uses per-side counts with cmax and
half-integer thresholds; RMC counts posterior ribs down to the diaphragm.

1. Posterior ribs are the ribs that run horizontally or slightly downward from the spine
   and are the denser set; anterior ribs run downward and medially toward the sternum and
   are fainter. Count posterior ribs only.
2. Count from the first rib downward. The first posterior rib is the highest rib arising
   from the spine above the clavicle; it is often partly obscured by the clavicle.
3. A rib counts as 1 if its inferior cortex, where it crosses the mid-clavicular line,
   lies above the hemidiaphragm outline at that same x position.
4. A rib counts as 0.5 if the hemidiaphragm outline at the mid-clavicular line crosses the
   rib between its superior and inferior cortex.
5. Count each side independently. `ribs_R` uses the right hemidiaphragm; `ribs_L` the left.
6. If ribs cannot be distinguished (overlying pathology, devices), record the count and tick
   `ribs_uncertain` for that side.

**[REVIEW]** Rules 3 and 4: the counting location (mid-clavicular line) and the half-rib
rule are not stated in the sources; vB24 only implies fractional counts through its
half-integer thresholds. Confirm the counting location and whether 0.5 steps are practical.

### 5.2 Scapula overlap (`scapula_R`, `scapula_L`: yes / no)

Source: EUR 1.1.3; RCR "Medial borders of scapulae to be outside the lung fields"; Wang26
"must not overlap with the lung fields".

1. The medial (vertebral) border of the scapula is the long, nearly vertical cortical line of
   the scapula closest to the spine.
2. `yes` if any part of the medial border projects within the CheXmask lung contour of that
   side; `no` if the entire medial border lies lateral to the contour or outside the image.
3. If the border is not identifiable, record `no` and tick `scapula_uncertain`.

**[REVIEW]** Rule 2 treats any overlap as a failure. Confirm whether a tolerance (for
example, overlap confined to the apex) is used in practice.

### 5.3 Exposure adequate (`exposure_ok`: yes / no)

Source: EUR 1.1.7 and 1.1.8; RMC "penetration": vertebral bodies just visible through the
heart.

1. `yes` if the thoracic vertebral bodies and the retrocardiac lung vessels are visible
   through the heart shadow, and peripheral lung vessels are visible.
2. `no` if the heart shadow is uniformly white with no spine visible (under-exposed) or the
   peripheral vessels are lost to black (over-exposed).

NIH PNGs are 8-bit processed images; exposure labels on them describe the processed image,
not the acquisition, and are reported as such.

### 5.4 Overall acceptable (`overall_ok`: yes / no)

Source: vB24 reader instruction, images scored per criterion with "OK", "inadequate",
"unacceptable"; RCR target that all criteria are met.

1. `yes` if no criterion in 6 is graded unacceptable.
2. Recorded independently of the per-criterion grades so that disagreement between the rule
   and the labeller's overall impression can be measured.

## 6. Grades

Source: vB24 three-level scale per criterion; collimation additionally too narrow or too
wide per border.

| Criterion   | OK                                                                 | Inadequate                                     | Unacceptable                                      |
| ----------- | ------------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------- |
| Inspiration | cmax ≥ 10 posterior ribs (EUR 1.1.1)                               | cmax 9 to 9.5                                  | cmax < 9                                          |
| Rotation    | Spinous process central between clavicle ends; α within ±0.2       | α between ±0.2 and ±0.41                       | α beyond ±0.41 (vB24 pooled threshold)            |
| Scapulae    | Neither medial border within the lung fields                       | —                                              | Either medial border within the lung fields       |
| Collimation | Each border within vB24 pooled limits                              | Any border within 25% of a limit               | Any border beyond a limit, or lung cut off        |
| Exposure    | Spine and retrocardiac vessels visible                             | —                                              | Not visible                                       |

Starting limits for collimation, in mm (vB24, PA, pooled): top 4 to 59, bottom 1 to 102,
E 6 to 67, W 4 to 56. These seed the labelling; learned thresholds replace them.

**[REVIEW]** The inadequate band for rotation (±0.2) and for collimation (25%) are
placeholders; vB24 reports no pooled inadequate thresholds. Confirm or set from the pilot.

Three worked examples per grade per criterion, with image identifiers, are added after the
50-image pilot (WP2).

## 7. Label Studio fields

| Field                      | Type       | Values                   |
| -------------------------- | ---------- | ------------------------ |
| `clavicle_R`, `clavicle_L` | keypoint   | x, y                     |
| `spine_1`, `spine_2`, `spine_3` | keypoint | x, y                   |
| `diaphragm_R`              | keypoint   | x, y                     |
| `ribs_R`, `ribs_L`         | number     | 0 to 12, step 0.5        |
| `scapula_R`, `scapula_L`   | choice     | yes, no                  |
| `exposure_ok`              | choice     | yes, no                  |
| `overall_ok`               | choice     | yes, no                  |
| `grade_inspiration`, `grade_rotation`, `grade_scapula`, `grade_collimation`, `grade_exposure` | choice | OK, inadequate, unacceptable |
| `clavicle_uncertain`, `spine_uncertain`, `diaphragm_uncertain`, `ribs_uncertain`, `scapula_uncertain`, `lung_contour_wrong` | checkbox | per side where applicable |
| `notes`                    | text       | free                     |

## 8. Rotation sign convention

α = (dR − dL) / (dR + dL), with dR and dL the perpendicular distances from `clavicle_R` and
`clavicle_L` to the spinous-process line (vB24). The clavicle end farther from the spine
marks the side the patient is rotated toward (RMC), so α > 0 is rotation to the patient's
right and α < 0 to the left. ECR20 uses the opposite sign; it is not used here.

## 9. AP and portable images (WP9)

EUR 16260 contains no chest AP criteria. Sorace et al. 2024 (Radiography 30:107) label AP
images as inadequate technique, adequate inspiration or inadequate inspiration; Wang26
includes 1,300 AP images under the same three positioning rules as PA. Rules for AP are
written during WP9 after the PA pilot and state, per criterion, whether it applies unchanged,
applies with a different threshold, or is not assessed.

## 10. Labeller training and review

1. Before the pilot, the labeller completes the RMC chest quality tutorial and the Radiopaedia
   chest radiograph technical assessment pages, and labels ten images under this protocol.
2. A qualified radiographer reviews this protocol and those ten images and resolves every
   **[REVIEW]** item. Changes are recorded in section 11.
3. The 50-image pilot follows; the protocol is revised to version 1.0 before full labelling.
4. Inter-rater agreement is measured on 100 images labelled by two qualified radiographers;
   intra-rater agreement on 200 images re-labelled after at least three weeks.

## 11. Revision history

| Version | Date       | Change                                                       |
| ------- | ---------- | ------------------------------------------------------------ |
| 0.1     | 2026-10-21 | Skeleton                                                     |
| 0.2     | 2026-10-21 | Rules drafted from sources; REVIEW items marked              |
