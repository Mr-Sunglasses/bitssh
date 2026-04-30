from unittest.mock import patch

import src.bitssh.utils
from src.bitssh.ui import draw_table


class TestDrawTable:
    def test_draws_table_with_rows(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        with patch("src.bitssh.ui.console") as mock_console:
            draw_table()
            assert mock_console.print.call_count == 1
            table_arg = mock_console.print.call_args[0][0]
            assert hasattr(table_arg, "title")
            assert "SSH Servers" in table_arg.title

    def test_draws_table_empty_config(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils,
            "CONFIG_FILE_PATH",
            mock_data_root_dir / "config_empty_and_only_comments.txt",
        )
        with patch("src.bitssh.ui.console") as mock_console:
            draw_table()
            mock_console.print.assert_called_once()

    def test_table_has_correct_columns(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        with patch("src.bitssh.ui.console") as mock_console:
            draw_table()
            table_arg = mock_console.print.call_args[0][0]
            column_names = [col.header for col in table_arg.columns]
            assert "Hostname" in column_names
            assert "Host" in column_names
            assert "Port" in column_names
            assert "User" in column_names

    def test_table_with_ports_data(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_with_ports.txt"
        )
        with patch("src.bitssh.ui.console") as mock_console:
            draw_table()
            table_arg = mock_console.print.call_args[0][0]
            assert table_arg.row_count == 2
