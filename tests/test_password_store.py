import stat

import pytest

from src.bitssh import crypto, password_store


@pytest.fixture(autouse=True)
def isolated_password_file(tmp_path, monkeypatch):
    path = tmp_path / "bitssh_passwords.json"
    monkeypatch.setattr(password_store, "PASSWORD_FILE_PATH", str(path))
    return path


def test_save_and_get_password_roundtrip():
    password_store.save_password("myserver", "hunter2")
    assert password_store.get_password("myserver") == "hunter2"


def test_has_password():
    assert password_store.has_password("myserver") is False
    password_store.save_password("myserver", "hunter2")
    assert password_store.has_password("myserver") is True


def test_get_password_returns_none_when_absent():
    assert password_store.get_password("missing-host") is None


def test_delete_password_removes_entry():
    password_store.save_password("myserver", "hunter2")
    password_store.delete_password("myserver")
    assert password_store.has_password("myserver") is False


def test_delete_password_is_noop_when_absent():
    password_store.delete_password("missing-host")  # should not raise


def test_password_file_is_created_with_restrictive_permissions(isolated_password_file):
    password_store.save_password("myserver", "hunter2")
    mode = stat.S_IMODE(isolated_password_file.stat().st_mode)
    assert mode == 0o600


def test_stored_file_never_contains_plaintext_password(isolated_password_file):
    password_store.save_password("myserver", "hunter2-plaintext")
    content = isolated_password_file.read_text()
    assert "hunter2-plaintext" not in content


def test_get_password_raises_when_undecryptable_on_this_device(monkeypatch):
    password_store.save_password("myserver", "hunter2")

    def _broken_decrypt(_entry):
        raise crypto.DecryptionError("nope")

    monkeypatch.setattr(crypto, "decrypt", _broken_decrypt)
    with pytest.raises(crypto.DecryptionError):
        password_store.get_password("myserver")


def test_multiple_hosts_independent():
    password_store.save_password("host-a", "pw-a")
    password_store.save_password("host-b", "pw-b")
    assert password_store.get_password("host-a") == "pw-a"
    assert password_store.get_password("host-b") == "pw-b"
