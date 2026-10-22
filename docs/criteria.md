# Criteria and metrics

## Source wording

European Commission. *European Guidelines on Quality Criteria for Diagnostic Radiographic
Images*, EUR 16260 EN, 1996. Chest PA projection, image criteria, verbatim:

| No.   | Criterion                                                                                                                   |
| ----- | --------------------------------------------------------------------------------------------------------------------------- |
| 1.1.1 | Performed at full inspiration (as assessed by the position of the ribs above the diaphragm — either 6 anteriorly or 10 posteriorly) and with suspended respiration |
| 1.1.2 | Symmetrical reproduction of the thorax as shown by central position of the spinous process between the medial ends of the clavicles |
| 1.1.3 | Medial border of the scapulae to be outside the lung fields                                                                |
| 1.1.4 | Reproduction of the whole rib cage above the diaphragm                                                                      |
| 1.1.5 | Visually sharp reproduction of the vascular pattern in the whole lung, particularly the peripheral vessels                   |
| 1.1.6 | Visually sharp reproduction of: (a) the trachea and proximal bronchi, (b) the borders of the heart and aorta, (c) the diaphragm and lateral costo-phrenic angles |
| 1.1.7 | Visualization of the retrocardiac lung and the mediastinum                                                                  |
| 1.1.8 | Visualization of the spine through the heart shadow                                                                         |

EUR 16260 defines no chest AP criteria. Chest lateral criteria exist but are out of scope.

The RCR AuditLive template *Adapted Anatomical Image Criteria for PA Chest Radiography*
(2011, reviewed 2022) restates 1.1.1 to 1.1.4 and adds appropriate exposure, visualisation
of both apices and lateral costophrenic angles, and appropriate collimation.

## Metrics

Definitions follow von Berg J, Hergaarden KFM, et al. *What patient positioning in chest X-ray
is still acceptable?* IMAGING 16(1):41–49, 2024, doi:10.1556/1647.2024.00187.

| Criterion   | Landmarks                                         | Metric                                                                                                   |
| ----------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Collimation | Lung-field contour; image border                  | Distance in mm from the bounding box of the lung contours to each image border. Positive = margin; negative = lung cut off. Four values: top, bottom, left, right (image sides). |
| Rotation    | Both medial clavicle ends; spinous-process line   | α = (dR − dL) / (dR + dL), d = perpendicular distance from each clavicle end to the line. Range [−1, 1]; 0 = balanced. |
| Inspiration | Posterior ribs; each hemidiaphragm dome           | cL, cR = posterior ribs above the left and right hemidiaphragm; cmax = max(cL, cR). |
| Scapulae    | Medial scapular border; lung contour              | Overlap yes/no per side.                                                                                 |

### Rotation sign

R and L are patient sides. The clavicle end farther from the spinous process marks the side
the patient is rotated toward, so α > 0 is rotation to the patient's right and α < 0 to the
left. The ECR 2020 poster C-05625 by the same group uses the opposite sign,
(dL − dR)/(dL + dR); cxr-qa uses the 2024 form everywhere.

### Collimation sides

von Berg 2024 labels borders N, S, E, W and does not state whether E and W are image or
patient sides. cxr-qa reports image sides and states so in every output.

### Inspiration

von Berg 2024 replaced the earlier sum c = cL + cR with cmax because pathology or anatomy
often complicates one side. Thresholds in that paper sit at half-integers, so partial ribs
are counted fractionally.

## Published thresholds (PA, pooled over seven readers, von Berg 2024)

Starting values for labelling only. cxr-qa learns its own thresholds from labels.

| Metric                 | Unacceptable when      |
| ---------------------- | ---------------------- |
| Top margin             | > 59 mm or < 4 mm      |
| Bottom margin          | > 102 mm or < 1 mm     |
| E margin               | > 67 mm or < 6 mm      |
| W margin               | > 56 mm or < 4 mm      |
| α                      | beyond ±0.41           |
| cmax                   | < 9.5 (9.0 also justified by the data) |

Reported AUC, OK versus unacceptable: collimation 0.97 to 0.99 per border, α 0.93,
cmax 0.97. Reader agreement: Cohen's kappa 0.36 to 0.50.

## Grades

Per criterion: OK, inadequate, unacceptable (von Berg 2024). Collimation adds too narrow or
too wide per border. Every grade carries a reason string.
