import os
import unittest
from unittest.mock import patch
from bitssh.utils import ConfigPathUtility

from typing import Dict, List, Tuple


class TestConfigPathUtility(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_config_data: str = """
Host testHost1
    HostName test.hostname1.com
    User testUser1
Host testHost2
    HostName test.hostname2.com
    User testUser2
"""

    def tearDown(self) -> None:
        if os.path.exists("config"):
            os.remove("config")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_content_success(self, mock_open, mock_exists) -> None:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected: Dict[str, Dict[str, str]] = {
            "testHost1": {"Hostname": "test.hostname1.com", "User": "testUser1"},
            "testHost2": {"Hostname": "test.hostname2.com", "User": "testUser2"},
        }
        result: ConfigPathUtility = ConfigPathUtility.get_config_content()
        self.assertEqual(result, expected)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_file_row_data(self, mock_open, mock_exists) -> None:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected_rows: List[Tuple[str, str, str, str]] = [
            ("test.hostname1.com", "testHost1", "22", "testUser1"),
            ("test.hostname2.com", "testHost2", "22", "testUser2"),
        ]
        rows: ConfigPathUtility = ConfigPathUtility.get_config_file_row_data()
        self.assertEqual(rows, expected_rows)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_file_host_data(self, mock_open, mock_exists) -> None:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected_hosts: List = [
            "🖥️  -> testHost1",
            "🖥️  -> testHost2",
        ]
        hosts: ConfigPathUtility = ConfigPathUtility.get_config_file_host_data()
        self.assertEqual(hosts, expected_hosts)


if __name__ == "__main__":
    unittest.main()
