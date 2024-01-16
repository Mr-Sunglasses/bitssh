import os

from typing import Dict
from bitssh.utils import get_config_path, get_config_content


def test_get_config_path() -> None:
    config_path: Dict[str, Dict[str, str]] = get_config_path()
    assert isinstance(config_path, str)
    assert os.path.isfile(config_path)


def test_get_config_content() -> None:
    test_config_file = "config"
    # Create a test config file with sample SSH server configurations
    with open(test_config_file, "w") as f:
        f.write(
            """
        Host test1
            Hostname example.com
            User user1
            port 22

        Host test2
            Hostname example.org
            User user2
            port 22
        """
        )

    config_content: Dict[str, Dict[str, str]] = get_config_content(
        config_file=test_config_file
    )
    assert isinstance(config_content, dict)
    assert "test1" in config_content
    assert "test2" in config_content
    assert config_content["test1"]["User"] == "user1"
    assert config_content["test2"]["Hostname"] == "example.org"

    # Clean up the test config file
    os.remove(test_config_file)
