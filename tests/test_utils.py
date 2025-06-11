import pytest
import os

from src.bitssh.utils import (
    get_config_content,
    get_config_file_host_data,
    get_config_file_row_data,
)
import src.bitssh.utils


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
                    "Hostname": "user_only",  # Should default to host name
                    "User": "user_only_user",
                    "Port": "22",
                },
                "minimal_host": {
                    "Hostname": "minimal_host",  # Should default to host name
                    "User": None,
                    "Port": "22",
                },
                "empty_host": {
                    "Hostname": "empty_host",  # Should default to host name
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
                "duplicate": {  # Current Implementation of Code always Picks the Last Entry
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
