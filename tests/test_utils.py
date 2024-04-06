import os
import unittest
from unittest.mock import patch
from bitssh.utils import ConfigPathUtility


class TestConfigPathUtility(unittest.TestCase):
    def setUp(self):
        self.mock_config_data = """
Host testHost1
    HostName test.hostname1.com
    User testUser1
Host testHost2
    HostName test.hostname2.com
    User testUser2
"""

    def tearDown(self):
        if os.path.exists("config"):
            os.remove("config")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_content_success(self, mock_open, mock_exists):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected = {
            "testHost1": {"Hostname": "test.hostname1.com", "User": "testUser1"},
            "testHost2": {"Hostname": "test.hostname2.com", "User": "testUser2"},
        }
        result = ConfigPathUtility.get_config_content()
        self.assertEqual(result, expected)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_file_row_data(self, mock_open, mock_exists):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected_rows = [
            ("test.hostname1.com", "testHost1", "22", "testUser1"),
            ("test.hostname2.com", "testHost2", "22", "testUser2"),
        ]
        rows = ConfigPathUtility.get_config_file_row_data()
        self.assertEqual(rows, expected_rows)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open")
    def test_get_config_file_host_data(self, mock_open, mock_exists):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            self.mock_config_data
        )
        expected_hosts = [
            "🖥️  -> testHost1",
            "🖥️  -> testHost2",
        ]
        hosts = ConfigPathUtility.get_config_file_host_data()
        self.assertEqual(hosts, expected_hosts)


if __name__ == "__main__":
    unittest.main()
