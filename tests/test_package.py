import importlib

import cxrqa


def test_version_is_semver() -> None:
    major, minor, patch = cxrqa.__version__.split(".")
    assert all(part.isdigit() for part in (major, minor, patch))


def test_subpackages_import() -> None:
    for name in ("io", "landmarks", "metrics", "grading", "report"):
        importlib.import_module(f"cxrqa.{name}")
