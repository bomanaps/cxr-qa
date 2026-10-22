"""NIH ChestX-ray14 metadata and pixel spacing.

Source: Wang X, Peng Y, Lu L, Lu Z, Bagheri M, Summers RM. ChestX-ray8: Hospital-scale chest
X-ray database and benchmarks on weakly-supervised classification and localization of common
thorax diseases. CVPR 2017. Metadata file ``Data_Entry_2017_v2020.csv`` from
https://nihcc.app.box.com/v/ChestXray-NIHCC.

The distributed PNGs are 1024 x 1024 pixels. The CSV records the width, height and pixel
spacing of the original acquisition, which is not square and not 1024 pixels. The effective
spacing of the PNG therefore differs per image and per axis and is derived here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

PNG_SIZE = 1024
"""Side length in pixels of every distributed ChestX-ray14 PNG."""

COLUMNS = {
    "Image Index": "image_id",
    "Finding Labels": "finding_labels",
    "Follow-up #": "follow_up",
    "Patient ID": "patient_id",
    "Patient Age": "age",
    "Patient Sex": "sex",
    "View Position": "view",
    "OriginalImage[Width": "original_width",
    "Height]": "original_height",
    "OriginalImagePixelSpacing[x": "original_spacing_x_mm",
    "y]": "original_spacing_y_mm",
}


@dataclass(frozen=True)
class PixelSpacing:
    """Physical size of one PNG pixel in millimetres, per axis."""

    x_mm: float
    y_mm: float


def effective_spacing(
    original_width: int,
    original_height: int,
    original_spacing_x_mm: float,
    original_spacing_y_mm: float,
    png_width: int = PNG_SIZE,
    png_height: int = PNG_SIZE,
) -> PixelSpacing:
    """Pixel spacing of the resized PNG given the original acquisition geometry.

    The PNG was produced by resampling the original ``original_width x original_height``
    image to ``png_width x png_height`` without preserving aspect ratio, so each axis
    scales independently.
    """
    if min(original_width, original_height, png_width, png_height) <= 0:
        raise ValueError("image dimensions must be positive")
    if min(original_spacing_x_mm, original_spacing_y_mm) <= 0:
        raise ValueError("pixel spacing must be positive")
    return PixelSpacing(
        x_mm=original_spacing_x_mm * original_width / png_width,
        y_mm=original_spacing_y_mm * original_height / png_height,
    )


def load_metadata(csv_path: Path) -> pd.DataFrame:
    """Load ``Data_Entry_2017_v2020.csv`` with normalised column names and derived spacing.

    Adds ``spacing_x_mm`` and ``spacing_y_mm`` for the 1024-pixel PNG.
    """
    frame = pd.read_csv(csv_path)
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"unexpected NIH metadata columns; missing {sorted(missing)}")
    frame = frame.rename(columns=COLUMNS)
    frame["spacing_x_mm"] = frame["original_spacing_x_mm"] * frame["original_width"] / PNG_SIZE
    frame["spacing_y_mm"] = frame["original_spacing_y_mm"] * frame["original_height"] / PNG_SIZE
    return frame


def adult_frontal(frame: pd.DataFrame, view: str, min_age: int = 18) -> pd.DataFrame:
    """Rows with the given view position (``"PA"`` or ``"AP"``) and age at or above ``min_age``."""
    if view not in {"PA", "AP"}:
        raise ValueError(f"view must be 'PA' or 'AP', got {view!r}")
    mask = (frame["view"] == view) & (frame["age"] >= min_age)
    return frame.loc[mask].reset_index(drop=True)
