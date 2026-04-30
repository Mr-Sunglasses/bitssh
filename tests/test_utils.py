import pytest

import src.bitssh.utils
from src.bitssh.utils import (
    _ensure_config_file,
    _validate_config_file,
    get_config_content,
    get_config_file_host_data,
    get_config_file_row_data,
    get_host_aliases,
    host_exists,
    remove_host_from_config,
    write_host_to_config,
)


@pytest.mark.parametrize(
    "file_to_test, expected_output",
    [
        (
            "config_data.txt",
            {
                "testHost1": {
                    "Hostname": "test.hostname1.com",
                    "User": "testUser1",
                    "Port": "22",
                },
                "testHost2": {
                    "Hostname": "test.hostname2.com",
                    "User": "testUser2",
                    "Port": "2222",
                },
            },
        ),
        (
            "config_with_ports.txt",
            {
                "server1": {
                    "Hostname": "192.168.1.100",
                    "User": "admin",
                    "Port": "2222",
                },
                "server2": {
                    "Hostname": "example.com",
                    "User": "root",
                    "Port": "443",
                },
            },
        ),
        (
            "config_mixed_case.txt",
            {
                "MixedCase": {
                    "Hostname": "mixed.case.com",
                    "User": "mixeduser",
                    "Port": "3333",
                },
                "lowercase": {
                    "Hostname": "UPPER.CASE.COM",
                    "User": "UPPERUSER",
                    "Port": "4444",
                },
            },
        ),
        (
            "config_incomplete.txt",
            {
                "complete_host": {
                    "Hostname": "complete.example.com",
                    "User": "complete_user",
                    "Port": "8080",
                },
                "hostname_only": {
                    "Hostname": "hostname.only.com",
                    "User": None,
                    "Port": "22",
                },
                "user_only": {
                    "Hostname": "user_only",
                    "User": "user_only_user",
                    "Port": "22",
                },
                "minimal_host": {
                    "Hostname": "minimal_host",
                    "User": None,
                    "Port": "22",
                },
                "empty_host": {
                    "Hostname": "empty_host",
                    "User": None,
                    "Port": "22",
                },
            },
        ),
        (
            "config_with_indentations.txt",
            {
                "indented1": {
                    "Hostname": "deeply.indented.com",
                    "User": "indented_user",
                    "Port": "5555",
                },
                "indented2": {
                    "Hostname": "normal.indent.com",
                    "User": "normal_user",
                    "Port": "6666",
                },
                "mixed_indent": {
                    "Hostname": "no.indent.com",
                    "User": "some_indent",
                    "Port": "7777",
                },
            },
        ),
        (
            "config_special_chars.txt",
            {
                "special-chars_123": {
                    "Hostname": "special-chars.example.com",
                    "Port": "9999",
                    "User": "user-with_underscores",
                },
                "numbers123": {
                    "Hostname": "10.0.0.1",
                    "User": "user123",
                    "Port": "22",
                },
            },
        ),
        ("config_empty_and_only_comments.txt", {}),
        (
            "config_malformed.txt",
            {
                "good_host": {
                    "Hostname": "good.example.com",
                    "User": "good_user",
                    "Port": "22",
                },
                "another_host": {
                    "Hostname": "another.example.com",
                    "User": "another_user",
                    "Port": "22",
                },
            },
        ),
        (
            "config_case_insensitive.txt",
            {
                "test1": {
                    "Hostname": "test1.com",
                    "User": "test1user",
                    "Port": "1111",
                },
                "test2": {
                    "Hostname": "test2.com",
                    "User": "test2user",
                    "Port": "2222",
                },
                "test3": {
                    "Hostname": "test3.com",
                    "User": "test3user",
                    "Port": "3333",
                },
            },
        ),
        (
            "config_duplicate.txt",
            {
                "duplicate": {
                    "Hostname": "second.example.com",
                    "User": "second_user",
                    "Port": "2222",
                }
            },
        ),
        (
            "config_whitespace.txt",
            {
                "whitespace_test": {
                    "Hostname": "whitespace.example.com",
                    "User": "whitespace_user",
                    "Port": "8888",
                },
                "tab_test": {
                    "Hostname": "tab.example.com",
                    "User": "tab_user",
                    "Port": "9999",
                },
            },
        ),
        (
            "config_complex.txt",
            {
                "complex": {
                    "Hostname": "complex.example.com",
                    "User": "complex_user",
                    "Port": "2020",
                },
            },
        ),
        (
            "config_inline_comments.txt",
            {
                "inline_test": {
                    "Hostname": "inline.example.com",
                    "User": "inline_user",
                    "Port": "5050",
                },
                "server-one": {
                    "Hostname": "server-one.example.com",
                    "User": "username",
                    "Port": "56",
                },
            },
        ),
        (
            "config_wildcard_filtering.txt",
            {
                "server-one": {
                    "Hostname": "server-one.example.com",
                    "User": "username",
                    "Port": "22",
                },
            },
        ),
        (
            "config_defaults.txt",
            {
                "minimal-server": {
                    "Hostname": "minimal.example.com",
                    "Port": "22",
                    "User": None,
                },
                "partial-server": {
                    "Hostname": "partial-server",
                    "User": "partial_user",
                    "Port": "22",
                },
            },
        ),
    ],
)
def test_get_config_content(
    mock_data_root_dir, monkeypatch, file_to_test: str, expected_output: dict
):
    mock_file_to_test = mock_data_root_dir / file_to_test
    monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", mock_file_to_test)

    actual_output = get_config_content()

    assert actual_output == expected_output


@pytest.mark.parametrize(
    "file_to_test, expected_rows",
    [
        (
            "config_data.txt",
            [
                ("test.hostname1.com", "testHost1", "22", "testUser1"),
                ("test.hostname2.com", "testHost2", "2222", "testUser2"),
            ],
        ),
        (
            "config_with_ports.txt",
            [
                ("192.168.1.100", "server1", "2222", "admin"),
                ("example.com", "server2", "443", "root"),
            ],
        ),
    ],
)
def test_get_config_file_row_data(
    mock_data_root_dir, monkeypatch, file_to_test: str, expected_rows: list
):
    mock_file_to_test = mock_data_root_dir / file_to_test
    monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", mock_file_to_test)

    actual_rows = get_config_file_row_data()

    assert actual_rows == expected_rows


@pytest.mark.parametrize(
    "file_to_test, expected_hosts",
    [
        (
            "config_data.txt",
            [
                "🖥️  -> testHost1",
                "🖥️  -> testHost2",
            ],
        ),
        (
            "config_mixed_case.txt",
            [
                "🖥️  -> MixedCase",
                "🖥️  -> lowercase",
            ],
        ),
    ],
)
def test_get_config_file_host_data(
    mock_data_root_dir, monkeypatch, file_to_test: str, expected_hosts: list
):
    mock_file_to_test = mock_data_root_dir / file_to_test
    monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", mock_file_to_test)

    actual_hosts: list[str] = get_config_file_host_data()

    assert actual_hosts == expected_hosts


class TestValidateConfigFile:
    def test_raises_when_file_not_found(self, tmp_path, monkeypatch):
        nonexistent = tmp_path / "no_such_file"
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", nonexistent)
        with pytest.raises(FileNotFoundError):
            _validate_config_file()

    def test_passes_when_file_exists(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        _validate_config_file()


class TestEnsureConfigFile:
    def test_creates_directory_and_file(self, tmp_path, monkeypatch):
        config_path = tmp_path / "ssh" / "config"
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)
        _ensure_config_file()
        assert config_path.exists()

    def test_does_not_overwrite_existing_file(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("Host existing\n    HostName 1.2.3.4\n", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)
        _ensure_config_file()
        assert config_path.read_text(encoding="utf-8") == "Host existing\n    HostName 1.2.3.4\n"

    def test_creates_file_in_existing_dir(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)
        _ensure_config_file()
        assert config_path.exists()


class TestHostExists:
    def test_returns_true_when_host_exists(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        assert host_exists("testHost1") is True

    def test_returns_false_when_host_not_found(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        assert host_exists("nonexistent") is False

    def test_returns_false_when_config_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", tmp_path / "no_such_file")
        assert host_exists("anything") is False


class TestGetHostAliases:
    def test_returns_host_aliases(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        aliases = get_host_aliases()
        assert aliases == ["testHost1", "testHost2"]

    def test_returns_empty_list_for_empty_config(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils,
            "CONFIG_FILE_PATH",
            mock_data_root_dir / "config_empty_and_only_comments.txt",
        )
        aliases = get_host_aliases()
        assert aliases == []


class TestWriteHostToConfig:
    def test_writes_new_host(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        write_host_to_config(host="myserver", hostname="192.168.1.1")

        content = config_path.read_text(encoding="utf-8")
        assert "Host myserver" in content
        assert "HostName 192.168.1.1" in content

    def test_writes_host_with_all_fields(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        write_host_to_config(
            host="myserver",
            hostname="192.168.1.1",
            user="root",
            port=2222,
            identity_file="~/.ssh/id_rsa",
        )

        content = config_path.read_text(encoding="utf-8")
        assert "Host myserver" in content
        assert "HostName 192.168.1.1" in content
        assert "User root" in content
        assert "Port 2222" in content
        assert "IdentityFile ~/.ssh/id_rsa" in content

    def test_does_not_write_port_22(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        write_host_to_config(host="myserver", hostname="192.168.1.1", port=22)

        content = config_path.read_text(encoding="utf-8")
        assert "Port" not in content

    def test_raises_error_when_host_already_exists(self, mock_data_root_dir, monkeypatch):
        monkeypatch.setattr(
            src.bitssh.utils, "CONFIG_FILE_PATH", mock_data_root_dir / "config_data.txt"
        )
        with pytest.raises(ValueError, match="already exists"):
            write_host_to_config(host="testHost1", hostname="1.2.3.4")

    def test_appends_to_existing_file(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text(
            "Host existing\n    HostName 1.2.3.4\n    User root\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        write_host_to_config(host="newhost", hostname="10.0.0.1", user="admin", port=22)

        content = config_path.read_text(encoding="utf-8")
        assert "Host existing" in content
        assert "Host newhost" in content
        assert "HostName 10.0.0.1" in content
        assert "User admin" in content

    def test_writes_user_none_not_included(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        write_host_to_config(host="myserver", hostname="1.2.3.4", user=None)

        content = config_path.read_text(encoding="utf-8")
        assert "User" not in content


class TestRemoveHostFromConfig:
    def test_removes_existing_host(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text(
            "Host myserver\n    HostName 192.168.1.1\n    User root\n\n"
            "Host other\n    HostName 10.0.0.1\n    User admin\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        remove_host_from_config("myserver")

        content = config_path.read_text(encoding="utf-8")
        assert "Host myserver" not in content
        assert "Host other" in content
        assert "HostName 10.0.0.1" in content

    def test_raises_error_when_host_not_found(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("Host myserver\n    HostName 192.168.1.1\n", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        with pytest.raises(ValueError, match="does not exist"):
            remove_host_from_config("nonexistent")

    def test_raises_error_when_config_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", tmp_path / "no_such_file")
        with pytest.raises(FileNotFoundError):
            remove_host_from_config("anything")

    def test_removes_last_host_leans_clean_file(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text("Host myserver\n    HostName 192.168.1.1\n", encoding="utf-8")
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        remove_host_from_config("myserver")

        content = config_path.read_text(encoding="utf-8")
        assert content.strip() == ""

    def test_removes_middle_host(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text(
            "Host first\n    HostName 1.1.1.1\n\n"
            "Host second\n    HostName 2.2.2.2\n\n"
            "Host third\n    HostName 3.3.3.3\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        remove_host_from_config("second")

        content = config_path.read_text(encoding="utf-8")
        assert "Host first" in content
        assert "Host third" in content
        assert "Host second" not in content
        assert "2.2.2.2" not in content

    def test_skips_to_next_host_block_correctly(self, tmp_path, monkeypatch):
        config_path = tmp_path / "config"
        config_path.write_text(
            "Host first\n    HostName 1.1.1.1\n\n"
            "Host second\n    HostName 2.2.2.2\n\n"
            "Host third\n    HostName 3.3.3.3\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(src.bitssh.utils, "CONFIG_FILE_PATH", config_path)

        remove_host_from_config("second")

        content = config_path.read_text(encoding="utf-8")
        assert "Host first" in content
        assert "HostName 1.1.1.1" in content
        assert "Host third" in content
        assert "HostName 3.3.3.3" in content
