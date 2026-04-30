import sys

from src.bitssh.argument_parser import Config


class TestConfigAddCommand:
    def test_add_interactive_no_flags(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "add"])
        config = Config()
        assert config.command == "add"
        assert config.host is None
        assert config.hostname is None
        assert config.user is None
        assert config.port is None
        assert config.identity_file is None
        assert config.is_add_interactive() is True
        assert config.is_add_non_interactive() is False

    def test_add_non_interactive_with_host_and_hostname(self, monkeypatch):
        monkeypatch.setattr(
            sys, "argv", ["bitssh", "add", "--host", "myserver", "--hostname", "192.168.1.1"]
        )
        config = Config()
        assert config.command == "add"
        assert config.host == "myserver"
        assert config.hostname == "192.168.1.1"
        assert config.is_add_interactive() is False
        assert config.is_add_non_interactive() is True

    def test_add_non_interactive_with_all_flags(self, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
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
                "--identity-file",
                "~/.ssh/id_rsa",
            ],
        )
        config = Config()
        assert config.command == "add"
        assert config.host == "srv"
        assert config.hostname == "10.0.0.1"
        assert config.user == "root"
        assert config.port == 2222
        assert config.identity_file == "~/.ssh/id_rsa"
        assert config.is_add_interactive() is False
        assert config.is_add_non_interactive() is True

    def test_add_partial_flags_not_interactive_not_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "add", "--host", "myserver"])
        config = Config()
        assert config.command == "add"
        assert config.host == "myserver"
        assert config.hostname is None
        assert config.is_add_interactive() is False
        assert config.is_add_non_interactive() is False


class TestConfigRemoveCommand:
    def test_remove_with_host_flag(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "remove", "--host", "myserver"])
        config = Config()
        assert config.command == "remove"
        assert config.host == ["myserver"]
        assert config.hosts == ["myserver"]

    def test_remove_with_multiple_host_flags(self, monkeypatch):
        monkeypatch.setattr(
            sys, "argv", ["bitssh", "remove", "--host", "srv1", "srv2", "srv3"]
        )
        config = Config()
        assert config.command == "remove"
        assert config.hosts == ["srv1", "srv2", "srv3"]

    def test_remove_hosts_property_with_none(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "remove"])
        config = Config()
        assert config.hosts == []

    def test_remove_without_host_flag(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "remove"])
        config = Config()
        assert config.command == "remove"
        assert config.host is None


class TestConfigVersion:
    def test_version_flag(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "--version"])
        config = Config()
        assert config.version is True

    def test_version_short_flag(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "-v"])
        config = Config()
        assert config.version is True

    def test_no_version_flag(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh", "add"])
        config = Config()
        assert config.version is False


class TestConfigDefaultCommand:
    def test_no_command(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh"])
        config = Config()
        assert config.command is None

    def test_no_command_default_values(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["bitssh"])
        config = Config()
        assert config.host is None
        assert config.hostname is None
        assert config.user is None
        assert config.port is None
        assert config.identity_file is None
        assert config.version is False
