"""Device-bound encryption helpers.

Passwords saved by bitssh are encrypted with a key derived from a
machine-specific identifier (platform UUID / machine-id / MAC address as a
last resort). The identifier itself is never written to disk. This means the
encrypted password file is only ever decryptable on the machine it was
created on -- copying it to another device (or handing it to an attacker who
doesn't have shell access on this machine) yields ciphertext that cannot be
turned back into a usable password.

This is "protect the data at rest / in transit" grade encryption, not a
substitute for full-disk encryption or an OS keychain: anyone with the
ability to run code as the local user can always ask bitssh to decrypt for
them, same as any secret unlocked automatically for that user.
"""

import base64
import os
import platform
import subprocess
import uuid
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

_PBKDF2_ITERATIONS = 480_000
_KEY_LENGTH = 32  # AES-256
_SALT_LENGTH = 16
_NONCE_LENGTH = 12


class DecryptionError(Exception):
    """Raised when a stored secret cannot be decrypted on this device."""


def _read_file_first_line(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            value = f.readline().strip()
            return value or None
    except OSError:
        return None


def _run(cmd: list) -> Optional[str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, check=False)
        return result.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _macos_platform_uuid() -> Optional[str]:
    output = _run(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"])
    if not output:
        return None
    for line in output.splitlines():
        if "IOPlatformUUID" in line:
            # Line looks like: "IOPlatformUUID" = "XXXXXXXX-XXXX-..."
            parts = line.split("=", 1)
            if len(parts) == 2:
                return parts[1].strip().strip('"')
    return None


def _linux_machine_id() -> Optional[str]:
    for path in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
        value = _read_file_first_line(path)
        if value:
            return value
    return None


def _windows_machine_guid() -> Optional[str]:
    output = _run(
        [
            "reg",
            "query",
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography",
            "/v",
            "MachineGuid",
        ]
    )
    if not output:
        return None
    for line in output.splitlines():
        if "MachineGuid" in line:
            parts = line.split()
            if parts:
                return parts[-1]
    return None


def get_device_id() -> str:
    """Best-effort, stable identifier for the current machine.

    Falls back to the MAC address (via uuid.getnode()) if no platform
    specific identifier can be found. The value is only ever used in-memory
    to derive an encryption key -- it is never persisted.
    """
    system = platform.system()
    device_id: Optional[str] = None

    if system == "Darwin":
        device_id = _macos_platform_uuid()
    elif system == "Linux":
        device_id = _linux_machine_id()
    elif system == "Windows":
        device_id = _windows_machine_guid()

    if not device_id:
        device_id = str(uuid.getnode())

    return device_id


def _derive_key(salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_LENGTH,
        salt=salt,
        iterations=_PBKDF2_ITERATIONS,
    )
    return kdf.derive(get_device_id().encode("utf-8"))


def encrypt(plaintext: str) -> dict:
    """Encrypt `plaintext`, returning a JSON-serializable dict.

    The dict is bound to this device: it can only be decrypted by calling
    `decrypt` on the same machine.
    """
    salt = os.urandom(_SALT_LENGTH)
    nonce = os.urandom(_NONCE_LENGTH)
    key = _derive_key(salt)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }


def decrypt(data: dict) -> str:
    """Reverse of `encrypt`. Raises DecryptionError on failure."""
    try:
        salt = base64.b64decode(data["salt"])
        nonce = base64.b64decode(data["nonce"])
        ciphertext = base64.b64decode(data["ciphertext"])
    except (KeyError, ValueError) as e:
        raise DecryptionError("Malformed encrypted entry.") from e

    key = _derive_key(salt)
    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    except Exception as e:  # cryptography raises InvalidTag on mismatch
        raise DecryptionError(
            "Could not decrypt this secret on this device. It was likely "
            "saved on a different machine."
        ) from e
    return plaintext.decode("utf-8")
