"""End-to-end tests of the WP1 data pipeline on the synthetic data directory."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

from cxrqa.io import chexmask, nih, overlay, sample
from cxrqa.io.image import sha256


def test_sample_cli_writes_valid_manifest(synthetic_data_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "manifest.csv"
    sample.main(
        ["--data-dir", str(synthetic_data_dir), "--out", str(out), "--n", "12", "--seed", "1"]
    )
    manifest = pd.read_csv(out)

    assert manifest.columns.tolist() == sample.MANIFEST_COLUMNS
    assert len(manifest) == 12
    assert manifest["patient_id"].is_unique
    assert (manifest["view"] == "PA").all()
    assert (manifest["age"] >= 18).all()
    assert (manifest["dice_rca_mean"] >= chexmask.RECOMMENDED_MIN_DICE_RCA).all()
    assert (manifest["source"] == "nih-chestxray14").all()

    metadata = nih.load_metadata(synthetic_data_dir / "nih" / "Data_Entry_2017_v2020.csv")
    joined = manifest.merge(metadata, on="image_id", suffixes=("", "_meta"))
    expected_x = joined["original_spacing_x_mm"] * joined["original_width"] / nih.PNG_SIZE
    expected_y = joined["original_spacing_y_mm"] * joined["original_height"] / nih.PNG_SIZE
    assert np.allclose(joined["spacing_x_mm"], expected_x)
    assert np.allclose(joined["spacing_y_mm"], expected_y)

    for image_id, digest in zip(manifest["image_id"], manifest["sha256"], strict=True):
        assert digest == sha256(synthetic_data_dir / "nih" / "images" / image_id)

    rerun = tmp_path / "again.csv"
    sample.main(
        ["--data-dir", str(synthetic_data_dir), "--out", str(rerun), "--n", "12", "--seed", "1"]
    )
    assert pd.read_csv(rerun)["image_id"].tolist() == manifest["image_id"].tolist()


def test_sample_without_hashes_and_with_too_large_n(
    synthetic_data_dir: Path, tmp_path: Path
) -> None:
    out = tmp_path / "nohash.csv"
    sample.main(["--data-dir", str(synthetic_data_dir), "--out", str(out), "--n", "5", "--no-hash"])
    assert pd.read_csv(out, keep_default_na=False)["sha256"].eq("").all()
    with pytest.raises(ValueError, match="eligible patients"):
        sample.main(["--data-dir", str(synthetic_data_dir), "--out", str(out), "--n", "10000"])


def test_chexmask_masks_agree_with_landmarks(synthetic_data_dir: Path) -> None:
    records = list(chexmask.iter_records(synthetic_data_dir / "chexmask" / "ChestX-Ray8.csv"))
    assert len(records) == 60
    for record in records[:5]:
        for name, points in (
            ("right_lung", record.right_lung),
            ("left_lung", record.left_lung),
            ("heart", record.heart),
        ):
            mask = record.mask(name)
            assert mask.shape == (record.height, record.width)
            centroid = points.mean(axis=0)
            assert mask[int(centroid[1]), int(centroid[0])]
            assert mask.sum() > 0.5 * np.ptp(points[:, 0]) * np.ptp(points[:, 1])
            assert (
                chexmask.encode_rle(mask)
                == {
                    "right_lung": record.right_lung_rle,
                    "left_lung": record.left_lung_rle,
                    "heart": record.heart_rle,
                }[name]
            )


def test_rle_matches_authors_convention() -> None:
    mask = chexmask.decode_rle("1 2 6 1", height=2, width=4)
    assert mask.tolist() == [[True, True, False, False], [False, True, False, False]]
    assert chexmask.encode_rle(mask) == "1 2 6 1"


def test_overlay_cli_draws_contours_for_manifest(synthetic_data_dir: Path, tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.csv"
    sample.main(
        ["--data-dir", str(synthetic_data_dir), "--out", str(manifest), "--n", "6", "--no-hash"]
    )
    out = tmp_path / "overlays"
    overlay.main(
        [
            "--data-dir",
            str(synthetic_data_dir),
            "--manifest",
            str(manifest),
            "--out",
            str(out),
            "--n",
            "4",
        ]
    )

    written = sorted(out.glob("*.png"))
    assert len(written) == 4
    records = chexmask.read_records(
        synthetic_data_dir / "chexmask" / "ChestX-Ray8.csv", {p.name for p in written}
    )
    for path in written:
        rgb = np.asarray(Image.open(path).convert("RGB"))
        assert rgb.shape == (1024, 1024, 3)
        record = records[path.name]
        for name, points in (("right_lung", record.right_lung), ("left_lung", record.left_lung)):
            x, y = (round(v) for v in points[0])
            assert tuple(rgb[y, x]) == overlay.COLOURS[name]


def test_overlay_rejects_size_mismatch(synthetic_data_dir: Path, tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.csv"
    sample.main(
        ["--data-dir", str(synthetic_data_dir), "--out", str(manifest), "--n", "1", "--no-hash"]
    )
    image_id = pd.read_csv(manifest)["image_id"].iloc[0]
    bad_root = tmp_path / "bad"
    (bad_root / "nih" / "images").mkdir(parents=True)
    (bad_root / "chexmask").mkdir()
    (bad_root / "chexmask" / "ChestX-Ray8.csv").write_bytes(
        (synthetic_data_dir / "chexmask" / "ChestX-Ray8.csv").read_bytes()
    )
    Image.fromarray(np.zeros((512, 512), dtype=np.uint8)).save(
        bad_root / "nih" / "images" / image_id
    )
    with pytest.raises(ValueError, match="CheXmask says"):
        overlay.main(
            [
                "--data-dir",
                str(bad_root),
                "--manifest",
                str(manifest),
                "--out",
                str(tmp_path / "o"),
                "--n",
                "1",
            ]
        )


@pytest.mark.data
def test_real_nih_metadata_matches_published_counts(data_dir: Path) -> None:
    metadata = nih.load_metadata(data_dir / "nih" / "Data_Entry_2017_v2020.csv")
    assert len(metadata) == 112_120
    assert metadata["patient_id"].nunique() == 30_805
    assert metadata["view"].value_counts().to_dict() == {"PA": 67_310, "AP": 44_810}
    assert len(nih.adult_frontal(metadata, "PA")) == 64_582
    assert metadata["spacing_x_mm"].between(0.1, 1.0).all()


@pytest.mark.data
def test_real_chexmask_first_rows_decode(data_dir: Path) -> None:
    path = data_dir / "chexmask" / "ChestX-Ray8.csv"
    if not path.exists():
        pytest.skip("CheXmask CSV not downloaded")
    for record, _ in zip(chexmask.iter_records(path), range(20), strict=False):
        assert (record.height, record.width) == (1024, 1024)
        assert record.landmarks.shape == (120, 2)
        assert -200 <= record.landmarks.min() and record.landmarks.max() <= 1224
        for name in ("right_lung", "left_lung", "heart"):
            assert record.mask(name).any()
