from unittest.mock import patch

import pytest

from src.bitssh import crypto


def test_encrypt_decrypt_roundtrip():
    data = crypto.encrypt("super-secret-password")
    assert crypto.decrypt(data) == "super-secret-password"


def test_ciphertext_is_not_plaintext():
    data = crypto.encrypt("super-secret-password")
    assert "super-secret-password" not in data["ciphertext"]


def test_encrypt_is_randomized():
    first = crypto.encrypt("same-password")
    second = crypto.encrypt("same-password")
    assert first["ciphertext"] != second["ciphertext"]
    assert first["salt"] != second["salt"]
    assert first["nonce"] != second["nonce"]


def test_decrypt_fails_on_different_device_id():
    with patch("src.bitssh.crypto.get_device_id", return_value="device-a"):
        data = crypto.encrypt("super-secret-password")

    with patch("src.bitssh.crypto.get_device_id", return_value="device-b"):
        with pytest.raises(crypto.DecryptionError):
            crypto.decrypt(data)


def test_decrypt_malformed_entry_raises():
    with pytest.raises(crypto.DecryptionError):
        crypto.decrypt({"salt": "not-base64!!", "nonce": "x", "ciphertext": "y"})


def test_get_device_id_returns_stable_value():
    assert crypto.get_device_id() == crypto.get_device_id()


def test_get_device_id_falls_back_to_mac_when_no_platform_id(monkeypatch):
    monkeypatch.setattr(crypto.platform, "system", lambda: "PlanNine")
    device_id = crypto.get_device_id()
    assert device_id == str(crypto.uuid.getnode())
