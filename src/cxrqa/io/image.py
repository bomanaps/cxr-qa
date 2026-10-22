"""Image file access."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import numpy.typing as npt
from PIL import Image


def load_grayscale(path: Path) -> npt.NDArray[np.uint8]:
    """Load a PNG as an 8-bit single-channel array of shape (height, width)."""
    with Image.open(path) as image:
        return np.asarray(image.convert("L"), dtype=np.uint8)


def sha256(path: Path) -> str:
    """Hex SHA-256 of a file's bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()
