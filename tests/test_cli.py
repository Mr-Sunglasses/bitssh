from unittest.mock import patch

from src.bitssh.argument_parser import Config
from src.bitssh.cli import _handle_add, _handle_remove, run


class TestHandleAdd:
    def test_interactive_mode_calls_add_host_prompt(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "add"])
        config = Config()
        with patch("src.bitssh.cli.add_host_prompt") as mock_prompt:
            _handle_add(config)
            mock_prompt.assert_called_once()

    def test_non_interactive_mode_calls_write_host_to_config(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv", ["bitssh", "add", "--host", "myserver", "--hostname", "192.168.1.1"]
        )
        config = Config()
        with patch("src.bitssh.cli.write_host_to_config") as mock_write:
            _handle_add(config)
            mock_write.assert_called_once_with(
                host="myserver",
                hostname="192.168.1.1",
                user=None,
                port=None,
                identity_file=None,
            )

    def test_non_interactive_with_all_flags(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "bitssh",
                "add",
                "--host",
                "srv",
                "--hostname",
                "10.0.0.1",
                "--user",
                "root",
                "--port",
                "2222",
            ],
        )
        config = Config()
        with patch("src.bitssh.cli.write_host_to_config") as mock_write:
            _handle_add(config)
            mock_write.assert_called_once_with(
                host="srv",
                hostname="10.0.0.1",
                user="root",
                port=2222,
                identity_file=None,
            )

    def test_non_interactive_duplicate_host_shows_error(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv", ["bitssh", "add", "--host", "myserver", "--hostname", "1.2.3.4"]
        )
        config = Config()
        with patch("src.bitssh.cli.write_host_to_config", side_effect=ValueError("already exists")):
            with patch("src.bitssh.cli.console") as mock_console:
                _handle_add(config)
                mock_console.print.assert_called()
                assert "Error" in mock_console.print.call_args[0][0] or "already exists" in str(
                    mock_console.print.call_args
                )

    def test_partial_flags_shows_error_message(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "add", "--host", "myserver"])
        config = Config()
        with patch("src.bitssh.cli.console") as mock_console:
            _handle_add(config)
            calls = mock_console.print.call_args_list
            error_calls = [c for c in calls if "Error" in str(c) or "Non-interactive" in str(c)]
            assert len(error_calls) > 0


class TestHandleRemove:
    def test_non_interactive_removes_host(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "remove", "--host", "myserver"])
        config = Config()
        with patch("src.bitssh.cli.remove_host_from_config") as mock_remove:
            with patch("src.bitssh.cli.console"):
                _handle_remove(config)
                mock_remove.assert_called_once_with("myserver")

    def test_non_interactive_host_not_found_shows_error(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "remove", "--host", "nonexistent"])
        config = Config()
        with patch(
            "src.bitssh.cli.remove_host_from_config", side_effect=ValueError("does not exist")
        ):
            with patch("src.bitssh.cli.console") as mock_console:
                _handle_remove(config)
                mock_console.print.assert_called()

    def test_interactive_mode_calls_remove_host_prompt(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "remove"])
        config = Config()
        with patch("src.bitssh.cli.remove_host_prompt") as mock_prompt:
            _handle_remove(config)
            mock_prompt.assert_called_once()


class TestRun:
    def test_version_flag_prints_version(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "--version"])
        with patch("builtins.print") as mock_print:
            run()
            mock_print.assert_called_once()
            assert "bitssh" in mock_print.call_args[0][0]

    def test_add_command_calls_handle_add(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "add"])
        with patch("src.bitssh.cli._handle_add") as mock_handle:
            run()
            mock_handle.assert_called_once()

    def test_remove_command_calls_handle_remove(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "remove", "--host", "myserver"])
        with patch("src.bitssh.cli._handle_remove") as mock_handle:
            run()
            mock_handle.assert_called_once()

    def test_no_command_draws_table_and_prompts(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh"])
        with (
            patch("src.bitssh.cli.draw_table") as mock_table,
            patch("src.bitssh.cli.ask_host_prompt") as mock_prompt,
        ):
            run()
            mock_table.assert_called_once()
            mock_prompt.assert_called_once()

    def test_keyboard_interrupt_silenced(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh"])
        with patch("src.bitssh.cli.draw_table", side_effect=KeyboardInterrupt):
            run()

    def test_generic_exception_handeled(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh"])
        with (
            patch("src.bitssh.cli.draw_table", side_effect=RuntimeError("boom")),
            patch("builtins.print") as mock_print,
        ):
            run()
            mock_print.assert_called()
            assert "boom" in mock_print.call_args[0][0]


class TestHandleAddErrors:
    def test_non_interactive_unexpected_error(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv", ["bitssh", "add", "--host", "myserver", "--hostname", "1.2.3.4"]
        )
        config = Config()
        with (
            patch("src.bitssh.cli.write_host_to_config", side_effect=RuntimeError("disk full")),
            patch("src.bitssh.cli.console") as mock_console,
        ):
            _handle_add(config)
            unexpected_calls = [
                c for c in mock_console.print.call_args_list if "Unexpected" in str(c)
            ]
            assert len(unexpected_calls) >= 1


class TestHandleRemoveErrors:
    def test_non_interactive_unexpected_error(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["bitssh", "remove", "--host", "myserver"])
        config = Config()
        with (
            patch("src.bitssh.cli.remove_host_from_config", side_effect=RuntimeError("disk full")),
            patch("src.bitssh.cli.console") as mock_console,
        ):
            _handle_remove(config)
            unexpected_calls = [
                c for c in mock_console.print.call_args_list if "Unexpected" in str(c)
            ]
            assert len(unexpected_calls) >= 1
