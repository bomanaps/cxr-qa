# Labelling protocol

Version 0.1, draft. Author: Mercy Boma. Not yet piloted.

This document defines every landmark and grade used in cxr-qa precisely enough that a second
labeller, given only this text, places the same points and assigns the same grades. Sections
marked TODO are written by the labelling lead during WP2 and revised after the 50-image pilot.

## 1. Scope

Adult (18 years and older) frontal chest radiographs. PA erect first; AP and portable images in
WP9 under section 8. Lateral, paediatric and non-chest images are excluded.

## 2. Image conventions

- Images are viewed in standard radiographic orientation: the patient's right is on the viewer's
  left. All left/right terms below refer to the **patient's** side.
- Coordinates are pixel (x, y) with origin at the top-left corner, x increasing to the right,
  y increasing downward, on the image at the resolution in which it was labelled.
- Distances in millimetres use the per-image pixel spacing recorded in the manifest.

## 3. Criteria and source wording

European Guidelines on Quality Criteria for Diagnostic Radiographic Images, EUR 16260 EN (1996),
chest PA projection, image criteria:

- 1.1.1 Performed at full inspiration (as assessed by the position of the ribs above the
  diaphragm — either 6 anteriorly or 10 posteriorly) and with suspended respiration
- 1.1.2 Symmetrical reproduction of the thorax as shown by central position of the spinous
  process between the medial ends of the clavicles
- 1.1.3 Medial border of the scapulae to be outside the lung fields
- 1.1.4 Reproduction of the whole rib cage above the diaphragm
- 1.1.7 Visualization of the retrocardiac lung and the mediastinum
- 1.1.8 Visualization of the spine through the heart shadow

Criteria 1.1.1 to 1.1.4 are measured in v1. Criteria 1.1.7 and 1.1.8 are labelled only
(exposure, section 7). Criteria 1.1.5 and 1.1.6 (sharpness) are out of scope.

## 4. Landmarks

### 4.1 Medial clavicle ends (2 points)

TODO: exact definition of the point placed, how to handle overlap with the first rib or
mediastinum, what to do when one end is obscured.

### 4.2 Spinous-process line (3 points)

TODO: which vertebral levels, how to place a point when the spinous process is not visible
through the mediastinum, how the line is fitted.

### 4.3 Right hemidiaphragm dome (1 point)

TODO: definition of the dome apex, handling of tented or flattened diaphragms.

### 4.4 Lung-field contour

Taken from CheXmask (Gaggion et al., Sci Data 2024), not labelled by hand. Images with
CheXmask Dice RCA (Mean) below 0.7 are excluded from the sample.

## 5. Count and choice fields

### 5.1 Posterior ribs above the right hemidiaphragm (integer)

TODO: counting rule, what counts as "above" (rib inferior border versus dome apex), handling
of partially visible ribs, left-side count.

### 5.2 Scapula overlap (yes/no, each side)

TODO: definition of the medial scapular border, what degree of projection over the lung
field counts as overlap.

### 5.3 Exposure adequate (yes/no)

TODO: retrocardiac lung and spine visibility rule, EUR 16260 criteria 1.1.7 and 1.1.8.

### 5.4 Overall acceptable (yes/no)

TODO: rule for combining the criteria into a single clinical judgement.

## 6. Grades

Each criterion receives one of: OK, inadequate, unacceptable, following von Berg et al. 2024.
Collimation additionally records too narrow or too wide per side.

TODO: three worked examples per grade per criterion, with image identifiers.

## 7. Exposure (labels only in v1)

TODO.

## 8. AP and portable images (WP9)

EUR 16260 contains no AP chest criteria. TODO: which PA criteria carry over, how scapula
overlap and cardiac magnification are treated, which landmarks remain labellable with lines
and tubes present.

## 9. Rotation sign convention

α = (dR − dL) / (dR + dL), where dR and dL are the perpendicular distances from the right and
left medial clavicle ends to the fitted spinous-process line. The clavicle end farther from
the spine marks the side the patient is rotated toward, so α > 0 means rotated to the patient's
right and α < 0 to the patient's left. This is the convention of von Berg et al. 2024; the
ECR 2020 poster C-05625 uses the opposite sign.

## 10. Revision history

| Version | Date        | Change        |
| ------- | ----------- | ------------- |
| 0.1     | 2026-10-21  | Skeleton      |
