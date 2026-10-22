"""Draw CheXmask contours on images for visual checking.

Run as ``python -m cxrqa.io.overlay``. Output PNGs go to a directory outside the repository.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd
from PIL import Image, ImageDraw

from cxrqa.io import chexmask
from cxrqa.io.image import load_grayscale

COLOURS = {"right_lung": (255, 80, 80), "left_lung": (80, 160, 255), "heart": (80, 220, 80)}


def draw_contours(
    image: npt.NDArray[np.uint8], record: chexmask.ChexmaskRecord, width: int = 2
) -> Image.Image:
    """RGB image with the three closed contours drawn in distinct colours."""
    canvas = Image.fromarray(image).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    for name, points in (
        ("right_lung", record.right_lung),
        ("left_lung", record.left_lung),
        ("heart", record.heart),
    ):
        closed = [tuple(p) for p in points.tolist()] + [tuple(points[0].tolist())]
        draw.line(closed, fill=COLOURS[name], width=width)
    return canvas


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=os.environ.get("DATA_DIR"))
    parser.add_argument("--manifest", type=Path, default=Path("data/manifests/nih_pa_sample.csv"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    if args.data_dir is None:
        parser.error("--data-dir or DATA_DIR is required")

    manifest = pd.read_csv(args.manifest)
    chosen = manifest.sample(n=min(args.n, len(manifest)), random_state=args.seed)
    ids = set(chosen["image_id"])
    records = chexmask.read_records(args.data_dir / "chexmask" / "ChestX-Ray8.csv", ids)
    args.out.mkdir(parents=True, exist_ok=True)
    for image_id in sorted(ids):
        image = load_grayscale(args.data_dir / "nih" / "images" / image_id)
        record = records[image_id]
        if image.shape != (record.height, record.width):
            raise ValueError(
                f"{image_id}: image is {image.shape}, CheXmask says {(record.height, record.width)}"
            )
        draw_contours(image, record).save(args.out / image_id)
    print(f"{len(ids)} overlays -> {args.out}")


if __name__ == "__main__":
    main()
