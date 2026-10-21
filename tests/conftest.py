import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Root of downloaded datasets; tests using it are marked `data` and skipped if absent."""
    value = os.environ.get("DATA_DIR")
    if value is None or not Path(value).is_dir():
        pytest.skip("DATA_DIR is not set or does not exist")
    return Path(value)
