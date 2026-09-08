from unittest.mock import MagicMock, patch

from src.bitssh.prompt import (
    _validate_host_alias,
    add_host_prompt,
    ask_host_prompt,
    remove_host_prompt,
)


class TestValidateHostAlias:
    def test_valid_alias_returns_true(self):
        assert _validate_host_alias("myserver") is True

    def test_empty_string_returns_false(self):
        assert _validate_host_alias("") is False

    def test_whitespace_only_returns_false(self):
        assert _validate_host_alias("   ") is False

    def test_none_returns_false(self):
        assert _validate_host_alias(None) is False

    def test_alias_with_spaces_returns_true(self):
        assert _validate_host_alias("my server") is True


class TestAddHostPrompt:
    def test_prints_header(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=False),
            patch("src.bitssh.prompt.write_host_to_config"),
        ):
            mock_inquirer.text.return_value.execute.side_effect = [
                "myserver",
                "1.2.3.4",
                "",
                "22",
                "",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            with patch("src.bitssh.prompt.console") as mock_console:
                add_host_prompt()
                header_calls = [
                    c for c in mock_console.print.call_args_list if "Add a New SSH Host" in str(c)
                ]
                assert len(header_calls) >= 1

    def test_existing_host_shows_error(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=True),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.text.return_value.execute.return_value = "myserver"
            add_host_prompt()
            error_calls = [
                c for c in mock_console.print.call_args_list if "already exists" in str(c)
            ]
            assert len(error_calls) >= 1

    def test_cancel_does_not_write(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=False),
            patch("src.bitssh.prompt.write_host_to_config") as mock_write,
        ):
            mock_inquirer.text.return_value.execute.side_effect = [
                "myserver",
                "1.2.3.4",
                "",
                "22",
                "",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = False

            with patch("src.bitssh.prompt.console"):
                add_host_prompt()

            mock_write.assert_not_called()

    def test_confirm_writes_host(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=False),
            patch("src.bitssh.prompt.write_host_to_config") as mock_write,
        ):
            mock_inquirer.text.return_value.execute.side_effect = [
                "myserver",
                "1.2.3.4",
                "root",
                "2222",
                "/key",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            with patch("src.bitssh.prompt.console"):
                add_host_prompt()

            mock_write.assert_called_once_with(
                host="myserver",
                hostname="1.2.3.4",
                user="root",
                port=2222,
                identity_file="/key",
            )

    def test_keyboard_interrupt_cancels(self):
        with patch("src.bitssh.prompt.inquirer") as mock_inquirer:
            mock_inquirer.text.return_value.execute.side_effect = KeyboardInterrupt()
            with patch("src.bitssh.prompt.console") as mock_console:
                add_host_prompt()
                cancelled_calls = [
                    c for c in mock_console.print.call_args_list if "Cancelled" in str(c)
                ]
                assert len(cancelled_calls) >= 1

    def test_value_error_shows_error(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=False),
            patch("src.bitssh.prompt.write_host_to_config", side_effect=ValueError("bad value")),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.text.return_value.execute.side_effect = [
                "myserver",
                "1.2.3.4",
                "",
                "22",
                "",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            add_host_prompt()
            error_calls = [c for c in mock_console.print.call_args_list if "Error" in str(c)]
            assert len(error_calls) >= 1

    def test_unexpected_error_shows_error(self):
        with (
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.host_exists", return_value=False),
            patch("src.bitssh.prompt.write_host_to_config", side_effect=RuntimeError("boom")),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.text.return_value.execute.side_effect = [
                "myserver",
                "1.2.3.4",
                "",
                "22",
                "",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            add_host_prompt()
            unexpected_calls = [
                c for c in mock_console.print.call_args_list if "Unexpected" in str(c)
            ]
            assert len(unexpected_calls) >= 1


class TestRemoveHostPrompt:
    def test_no_hosts_prints_message(self):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=[]),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            remove_host_prompt()
            msg_calls = [c for c in mock_console.print.call_args_list if "No hosts" in str(c)]
            assert len(msg_calls) >= 1

    def test_select_none_returns_early(self):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = []
            with patch("src.bitssh.prompt.console"):
                remove_host_prompt()

            mock_inquirer.checkbox.assert_called_once()

    def test_cancel_confirm_does_not_remove(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "myserver": {"Hostname": "1.2.3.4", "User": "root", "Port": "22"}
                },
            ),
            patch("src.bitssh.prompt.remove_host_from_config") as mock_remove,
            patch("src.bitssh.prompt.console"),
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> myserver"
            ]
            mock_inquirer.confirm.return_value.execute.return_value = False

            remove_host_prompt()
            mock_remove.assert_not_called()

    def test_confirm_removes_single_host(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "myserver": {"Hostname": "1.2.3.4", "User": "root", "Port": "22"}
                },
            ),
            patch("src.bitssh.prompt.remove_host_from_config") as mock_remove,
            patch("src.bitssh.prompt.console"),
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> myserver"
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            remove_host_prompt()
            mock_remove.assert_called_once_with("myserver")

    def test_confirm_removes_multiple_hosts(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> srv1", "🖥️  -> srv2"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "srv1": {"Hostname": "1.1.1.1", "User": "root", "Port": "22"},
                    "srv2": {"Hostname": "2.2.2.2", "User": "admin", "Port": "2222"},
                },
            ),
            patch("src.bitssh.prompt.remove_host_from_config") as mock_remove,
            patch("src.bitssh.prompt.console"),
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> srv1",
                "🖥️  -> srv2",
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            remove_host_prompt()
            assert mock_remove.call_count == 2
            mock_remove.assert_any_call("srv1")
            mock_remove.assert_any_call("srv2")

    def test_displays_hosts_table_before_removal(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "myserver": {"Hostname": "1.2.3.4", "User": "root", "Port": "22"}
                },
            ),
            patch("src.bitssh.prompt.remove_host_from_config"),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> myserver"
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            remove_host_prompt()
            table_calls = [
                c
                for c in mock_console.print.call_args_list
                if "table" in str(c).lower() or "Table" in str(c)
            ]
            assert len(table_calls) >= 1

    def test_keyboard_interrupt_cancels(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                side_effect=KeyboardInterrupt,
            ),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            remove_host_prompt()
            cancelled_calls = [
                c for c in mock_console.print.call_args_list if "Cancelled" in str(c)
            ]
            assert len(cancelled_calls) >= 1

    def test_invalid_format_shows_error(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "no-delimiter-here"
            ]

            remove_host_prompt()
            error_calls = [c for c in mock_console.print.call_args_list if "Error" in str(c)]
            assert len(error_calls) >= 1

    def test_value_error_during_removal(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "myserver": {"Hostname": "1.2.3.4", "User": "root", "Port": "22"}
                },
            ),
            patch(
                "src.bitssh.prompt.remove_host_from_config",
                side_effect=ValueError("not found"),
            ),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> myserver"
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            remove_host_prompt()
            error_calls = [c for c in mock_console.print.call_args_list if "Error" in str(c)]
            assert len(error_calls) >= 1

    def test_unexpected_error_during_removal(self):
        with (
            patch(
                "src.bitssh.prompt.get_config_file_host_data",
                return_value=["🖥️  -> myserver"],
            ),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch(
                "src.bitssh.prompt.get_config_content",
                return_value={
                    "myserver": {"Hostname": "1.2.3.4", "User": "root", "Port": "22"}
                },
            ),
            patch(
                "src.bitssh.prompt.remove_host_from_config",
                side_effect=RuntimeError("disk error"),
            ),
            patch("src.bitssh.prompt.console") as mock_console,
        ):
            mock_inquirer.checkbox.return_value.execute.return_value = [
                "🖥️  -> myserver"
            ]
            mock_inquirer.confirm.return_value.execute.return_value = True

            remove_host_prompt()
            unexpected_calls = [
                c for c in mock_console.print.call_args_list if "Unexpected" in str(c)
            ]
            assert len(unexpected_calls) >= 1


class TestAskHostPrompt:
    def test_null_selection_returns(self):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
        ):
            mock_inquirer.fuzzy.return_value.execute.return_value = None
            with patch("src.bitssh.prompt.console"):
                ask_host_prompt()

    def test_connects_to_selected_host(self):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.subprocess") as mock_subprocess,
        ):
            mock_inquirer.fuzzy.return_value.execute.return_value = "🖥️  -> myserver"
            mock_subprocess.run.return_value = MagicMock(returncode=0)

            with patch("src.bitssh.prompt.os.name", "posix"), patch("src.bitssh.prompt.console"):
                ask_host_prompt()

    def test_invalid_format_raises_error(self, capsys):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
        ):
            mock_inquirer.fuzzy.return_value.execute.return_value = "no-delimiter"

            with patch("src.bitssh.prompt.console"):
                ask_host_prompt()

            captured = capsys.readouterr()
            assert "Invalid" in captured.out

    def test_windows_clear_command(self):
        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.subprocess") as mock_subprocess,
            patch("src.bitssh.prompt.os.name", "nt"),
            patch("src.bitssh.prompt.console"),
        ):
            mock_inquirer.fuzzy.return_value.execute.return_value = "🖥️  -> myserver"
            mock_subprocess.run.return_value = MagicMock(returncode=0)

            ask_host_prompt()

            cls_calls = [c for c in mock_subprocess.run.call_args_list if c[0][0] == ["cls"]]
            assert len(cls_calls) >= 1

    def test_called_process_error_handling(self):
        from subprocess import CalledProcessError as RealCalledProcessError

        with (
            patch("src.bitssh.prompt.get_config_file_host_data", return_value=["🖥️  -> myserver"]),
            patch("src.bitssh.prompt.inquirer") as mock_inquirer,
            patch("src.bitssh.prompt.subprocess.run") as mock_run,
            patch("src.bitssh.prompt.os.name", "posix"),
            patch("src.bitssh.prompt.console") as mock_console,
            patch("src.bitssh.prompt.subprocess.CalledProcessError", RealCalledProcessError),
        ):
            mock_inquirer.fuzzy.return_value.execute.return_value = "🖥️  -> myserver"
            mock_run.side_effect = RealCalledProcessError(1, "ssh", output="connection failed")

            ask_host_prompt()

            printed = " ".join(str(c.args[0]) for c in mock_console.print.call_args_list)
            assert "Connection failed" in printed
            assert "1" in printed
