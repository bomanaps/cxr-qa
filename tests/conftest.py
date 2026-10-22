"""Shared fixtures.

``synthetic_data_dir`` builds a complete miniature of the real data layout: an NIH metadata
CSV, 1024 x 1024 PNGs, and a CheXmask CSV whose landmarks and run-length masks are generated
from the same polygons, so every stage of the pipeline can be exercised end to end.

``data_dir`` points at real downloads and is used only by tests marked ``data``.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw

from cxrqa.io import chexmask

N_IMAGES = 60
N_PATIENTS = 24
PNG = 1024


def _polygon(centre: tuple[float, float], rx: float, ry: float, n: int) -> np.ndarray:
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.column_stack([centre[0] + rx * np.cos(angles), centre[1] + ry * np.sin(angles)])


def _mask_from_polygon(points: np.ndarray) -> np.ndarray:
    canvas = Image.new("1", (PNG, PNG), 0)
    ImageDraw.Draw(canvas).polygon([tuple(p) for p in points.tolist()], fill=1)
    return np.asarray(canvas, dtype=bool)


@pytest.fixture(scope="session")
def synthetic_data_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("data")
    nih = root / "nih"
    images = nih / "images"
    images.mkdir(parents=True)
    (root / "chexmask").mkdir()
    rng = np.random.default_rng(20261021)

    nih_rows = []
    cx_rows = []
    for i in range(N_IMAGES):
        image_id = f"{i:08d}_000.png"
        patient = i % N_PATIENTS
        age = int(rng.integers(5, 90))
        view = "PA" if i % 4 else "AP"
        width, height = int(rng.choice([2048, 2500, 3000])), int(rng.choice([2048, 2749]))
        spacing = float(rng.choice([0.143, 0.168, 0.194]))
        nih_rows.append(
            f"{image_id},No Finding,0,{patient},{age},F,{view},{width},{height},{spacing},{spacing}"
        )

        shift = float(rng.uniform(-40, 40))
        right = _polygon((330 + shift, 520), 150, 300, chexmask.N_RIGHT_LUNG)
        left = _polygon((690 + shift, 520), 150, 300, chexmask.N_LEFT_LUNG)
        heart = _polygon((560 + shift, 700), 130, 150, chexmask.N_HEART)
        landmarks = ",".join(f"{v:.1f}" for v in np.vstack([right, left, heart]).ravel())
        dice = float(rng.uniform(0.5, 1.0))
        cx_rows.append(
            f'{image_id},{dice:.4f},{dice + 0.01:.4f},"{landmarks}",'
            f"{chexmask.encode_rle(_mask_from_polygon(left))},"
            f"{chexmask.encode_rle(_mask_from_polygon(right))},"
            f"{chexmask.encode_rle(_mask_from_polygon(heart))},{PNG},{PNG}"
        )

        pixels = rng.integers(0, 255, size=(PNG, PNG), dtype=np.uint8)
        Image.fromarray(pixels).save(images / image_id)

    (nih / "Data_Entry_2017_v2020.csv").write_text(
        "Image Index,Finding Labels,Follow-up #,Patient ID,Patient Age,Patient Sex,"
        "View Position,OriginalImage[Width,Height],OriginalImagePixelSpacing[x,y]\n"
        + "\n".join(nih_rows)
        + "\n"
    )
    (root / "chexmask" / "ChestX-Ray8.csv").write_text(
        "Image Index,Dice RCA (Mean),Dice RCA (Max),Landmarks,Left Lung,Right Lung,Heart,"
        "Height,Width\n" + "\n".join(cx_rows) + "\n"
    )
    return root


@pytest.fixture(scope="session")
def data_dir() -> Path:
    value = os.environ.get("DATA_DIR")
    if value is None or not Path(value).is_dir():
        pytest.skip("DATA_DIR is not set or does not exist")
    return Path(value)
