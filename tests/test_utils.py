import os
import unittest
from typing import Dict, List, Tuple
from unittest.mock import mock_open, patch

from src.bitssh.utils import (
    get_config_content,
    get_config_file_host_data,
    get_config_file_row_data,
)


class TestConfigPathUtility(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_config_data: str = """
Host testHost1
    HostName test.hostname1.com
    User testUser1
Host testHost2
    Hostname test.hostname2.com
    User testUser2
"""

    @patch("os.path.exists", return_value=True)
    def test_get_config_content_success(self, mock_exists) -> None:
        with patch("builtins.open", mock_open(read_data=self.mock_config_data)):
            expected: Dict[str, Dict[str, str]] = {
                "testHost1": {
                    "Hostname": "test.hostname1.com",
                    "User": "testUser1",
                    "Port": "22",
                },
                "testHost2": {
                    "Hostname": "test.hostname2.com",
                    "User": "testUser2",
                    "Port": "22",
                },
            }
            result = get_config_content()
            self.assertEqual(result, expected)

    @patch("os.path.exists", return_value=True)
    def test_get_config_file_row_data(self, mock_exists) -> None:
        with patch("builtins.open", mock_open(read_data=self.mock_config_data)):
            expected_rows: List[Tuple[str, str, str, str]] = [
                ("test.hostname1.com", "testHost1", "22", "testUser1"),
                ("test.hostname2.com", "testHost2", "22", "testUser2"),
            ]
            rows = get_config_file_row_data()
            self.assertEqual(rows, expected_rows)

    @patch("os.path.exists", return_value=True)
    def test_get_config_file_host_data(self, mock_exists) -> None:
        with patch("builtins.open", mock_open(read_data=self.mock_config_data)):
            expected_hosts: List[str] = [
                "🖥️  -> testHost1",
                "🖥️  -> testHost2",
            ]
            hosts: List[str] = get_config_file_host_data()
            self.assertEqual(hosts, expected_hosts)

    def test_file_not_found_error(self) -> None:
        with (
            patch("os.path.exists", return_value=False),
            self.assertRaises(FileNotFoundError),
        ):
            get_config_content()
