"""CheXmask lung and heart contours and masks.

Source: Gaggion N, Mosquera C, Mansilla L, Saidman JM, Aineseder M, Milone DH, Ferrante E.
CheXmask: a large-scale dataset of anatomical segmentation masks for multi-center chest x-ray
images. Sci Data 11, 511 (2024). doi:10.1038/s41597-024-03358-1. PhysioNet v1.0.0, CC BY 4.0.

File format (one CSV per source dataset, ``OriginalResolution`` folder): columns
``Image Index``, ``Dice RCA (Mean)``, ``Dice RCA (Max)``, ``Landmarks``, ``Left Lung``,
``Right Lung``, ``Heart``, ``Height``, ``Width``.

``Landmarks`` is a comma-separated list of 240 numbers forming 120 (x, y) points: indices
0-43 right lung, 44-93 left lung, 94-119 heart (ordering from the authors' Example.ipynb).
Mask columns are run-length encoded as space-separated ``start length`` pairs over the
row-major flattened image, with 1-based starts (``DataPostprocessing/utils.py``).

The authors recommend using masks with ``Dice RCA (Mean)`` of at least 0.7.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd

N_RIGHT_LUNG = 44
N_LEFT_LUNG = 50
N_HEART = 26
N_LANDMARKS = N_RIGHT_LUNG + N_LEFT_LUNG + N_HEART

RECOMMENDED_MIN_DICE_RCA = 0.7

_INDEX_COLUMNS = ["Image Index", "Dice RCA (Mean)", "Dice RCA (Max)", "Height", "Width"]


@dataclass(frozen=True)
class ChexmaskRecord:
    """One image's CheXmask annotation."""

    image_id: str
    dice_rca_mean: float
    dice_rca_max: float
    height: int
    width: int
    landmarks: npt.NDArray[np.float64]
    """Shape (120, 2), columns x then y, in pixels of the ``height x width`` image."""
    left_lung_rle: str
    right_lung_rle: str
    heart_rle: str

    @property
    def right_lung(self) -> npt.NDArray[np.float64]:
        """Right-lung contour points, shape (44, 2)."""
        return self.landmarks[:N_RIGHT_LUNG]

    @property
    def left_lung(self) -> npt.NDArray[np.float64]:
        """Left-lung contour points, shape (50, 2)."""
        return self.landmarks[N_RIGHT_LUNG : N_RIGHT_LUNG + N_LEFT_LUNG]

    @property
    def heart(self) -> npt.NDArray[np.float64]:
        """Heart contour points, shape (26, 2)."""
        return self.landmarks[N_RIGHT_LUNG + N_LEFT_LUNG :]

    def mask(self, structure: str) -> npt.NDArray[np.bool_]:
        """Decode the mask for ``"left_lung"``, ``"right_lung"`` or ``"heart"``."""
        rle = {
            "left_lung": self.left_lung_rle,
            "right_lung": self.right_lung_rle,
            "heart": self.heart_rle,
        }[structure]
        return decode_rle(rle, self.height, self.width)


def decode_rle(rle: str, height: int, width: int) -> npt.NDArray[np.bool_]:
    """Decode a CheXmask run-length string to a boolean mask of shape (height, width)."""
    flat = np.zeros(height * width, dtype=np.bool_)
    if rle.strip():
        runs = np.fromstring(rle, dtype=np.int64, sep=" ")
        if runs.size % 2:
            raise ValueError("RLE must contain start/length pairs")
        starts = runs[::2] - 1
        lengths = runs[1::2]
        if int(np.min(starts)) < 0 or int(np.max(starts + lengths)) > flat.size:
            raise ValueError("RLE runs fall outside the image")
        for start, length in zip(starts, lengths, strict=True):
            flat[start : start + length] = True
    return flat.reshape(height, width)


def encode_rle(mask: npt.NDArray[np.bool_]) -> str:
    """Inverse of :func:`decode_rle`, matching the authors' ``get_RLE_from_mask``."""
    pixels = np.concatenate([[0], mask.ravel().astype(np.int64), [0]])
    changes = np.flatnonzero(pixels[1:] != pixels[:-1]) + 1
    changes[1::2] -= changes[::2]
    return " ".join(str(int(v)) for v in changes)


def parse_landmarks(text: str) -> npt.NDArray[np.float64]:
    """Parse the ``Landmarks`` column into an array of shape (120, 2)."""
    values = np.fromstring(text, dtype=np.float64, sep=",")
    if values.size != 2 * N_LANDMARKS:
        raise ValueError(f"expected {2 * N_LANDMARKS} landmark values, got {values.size}")
    return values.reshape(N_LANDMARKS, 2)


def _record_from_row(row: dict[str, str]) -> ChexmaskRecord:
    return ChexmaskRecord(
        image_id=row["Image Index"],
        dice_rca_mean=float(row["Dice RCA (Mean)"]),
        dice_rca_max=float(row["Dice RCA (Max)"]),
        height=int(row["Height"]),
        width=int(row["Width"]),
        landmarks=parse_landmarks(row["Landmarks"]),
        left_lung_rle=row["Left Lung"],
        right_lung_rle=row["Right Lung"],
        heart_rle=row["Heart"],
    )


def iter_records(csv_path: Path) -> Iterator[ChexmaskRecord]:
    """Stream records from a CheXmask CSV without loading the whole file."""
    csv.field_size_limit(sys.maxsize)
    with csv_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            yield _record_from_row(row)


def read_records(csv_path: Path, image_ids: set[str]) -> dict[str, ChexmaskRecord]:
    """Return records for the given image identifiers, streamed from the CSV."""
    return {r.image_id: r for r in iter_records(csv_path) if r.image_id in image_ids}


def read_index(csv_path: Path) -> pd.DataFrame:
    """Lightweight table of image_id, Dice RCA scores and image size, without masks."""
    frame = pd.read_csv(csv_path, usecols=_INDEX_COLUMNS)
    return frame.rename(
        columns={
            "Image Index": "image_id",
            "Dice RCA (Mean)": "dice_rca_mean",
            "Dice RCA (Max)": "dice_rca_max",
            "Height": "height",
            "Width": "width",
        }
    )
