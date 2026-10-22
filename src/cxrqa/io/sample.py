"""Stratified sample of adult PA ChestX-ray14 images for labelling.

Run as ``python -m cxrqa.io.sample``. Writes a manifest of image identifiers, metadata
and file hashes; never images.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd

from cxrqa.io import chexmask, nih
from cxrqa.io.image import sha256

AGE_BINS = [18, 40, 60, 200]
AGE_LABELS = ["18-39", "40-59", "60+"]
DICE_QUANTILES = 3

MANIFEST_COLUMNS = [
    "image_id",
    "source",
    "patient_id",
    "age",
    "sex",
    "view",
    "original_width",
    "original_height",
    "spacing_x_mm",
    "spacing_y_mm",
    "dice_rca_mean",
    "dice_rca_max",
    "stratum",
    "sha256",
]


def candidates(
    metadata: pd.DataFrame,
    index: pd.DataFrame,
    view: str = "PA",
    min_age: int = 18,
    min_dice: float = chexmask.RECOMMENDED_MIN_DICE_RCA,
) -> pd.DataFrame:
    """Adult images of the given view with an acceptable CheXmask, one table."""
    frontal = nih.adult_frontal(metadata, view=view, min_age=min_age)
    good = index.loc[
        index["dice_rca_mean"] >= min_dice, ["image_id", "dice_rca_mean", "dice_rca_max"]
    ]
    merged = frontal.merge(good, on="image_id", how="inner")
    age_bin = pd.cut(merged["age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    dice_bin = pd.qcut(merged["dice_rca_mean"], q=DICE_QUANTILES, labels=False, duplicates="drop")
    merged["stratum"] = age_bin.astype(str) + "/dice" + dice_bin.astype(str)
    return merged


def stratified_sample(frame: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    """Sample ``n`` rows, at most one per patient, spread evenly across ``stratum``.

    Patients are first reduced to one randomly chosen image each so that no patient
    appears twice; strata are then sampled proportionally to their patient counts.
    """
    rng = np.random.default_rng(seed)
    one_per_patient = (
        frame.sample(frac=1.0, random_state=int(rng.integers(2**31)))
        .drop_duplicates("patient_id")
        .reset_index(drop=True)
    )
    if len(one_per_patient) < n:
        raise ValueError(f"only {len(one_per_patient)} eligible patients for a sample of {n}")
    counts = one_per_patient["stratum"].value_counts()
    quota = (counts / counts.sum() * n).round().astype(int)
    quota.iloc[0] += n - int(quota.sum())
    parts = []
    for stratum, available, wanted in zip(
        counts.index.tolist(), counts.tolist(), quota.tolist(), strict=True
    ):
        members = one_per_patient[one_per_patient["stratum"] == stratum]
        parts.append(
            members.sample(n=min(wanted, available), random_state=int(rng.integers(2**31)))
        )
    chosen: pd.DataFrame = pd.concat(parts)
    return chosen.sort_values("image_id").reset_index(drop=True)


def build_manifest(sample: pd.DataFrame, image_dir: Path | None, source: str) -> pd.DataFrame:
    """Manifest rows for the sample; file hashes are filled when ``image_dir`` is given."""
    manifest = sample.copy()
    manifest["source"] = source
    if image_dir is None:
        manifest["sha256"] = ""
    else:
        manifest["sha256"] = [sha256(image_dir / image_id) for image_id in manifest["image_id"]]
    return manifest[MANIFEST_COLUMNS]


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=os.environ.get("DATA_DIR"))
    parser.add_argument("--out", type=Path, default=Path("data/manifests/nih_pa_sample.csv"))
    parser.add_argument("--n", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--view", choices=["PA", "AP"], default="PA")
    parser.add_argument(
        "--no-hash",
        action="store_true",
        help="skip SHA-256 of image files (images not yet on disk)",
    )
    args = parser.parse_args(argv)
    if args.data_dir is None:
        parser.error("--data-dir or DATA_DIR is required")

    metadata = nih.load_metadata(args.data_dir / "nih" / "Data_Entry_2017_v2020.csv")
    index = chexmask.read_index(args.data_dir / "chexmask" / "ChestX-Ray8.csv")
    pool = candidates(metadata, index, view=args.view)
    sample = stratified_sample(pool, n=args.n, seed=args.seed)
    image_dir = None if args.no_hash else args.data_dir / "nih" / "images"
    manifest = build_manifest(sample, image_dir, source="nih-chestxray14")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(args.out, index=False)
    print(f"{len(manifest)} rows -> {args.out}")
    print(manifest["stratum"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
