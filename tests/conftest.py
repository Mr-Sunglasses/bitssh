from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def mock_data_root_dir() -> Path:
    test_root = Path(__file__).parent.resolve()
    return test_root / "data"
