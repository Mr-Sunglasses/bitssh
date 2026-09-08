"""Storage for optional, device-encrypted SSH host passwords.

Passwords are stored separately from ~/.ssh/config (which is plain text and
often synced/backed up) in a small JSON file containing only
AES-256-GCM ciphertext keyed by host alias. See `crypto.py` for the
encryption scheme.
"""

import json
import os
from typing import Optional

from . import crypto

PASSWORD_FILE_PATH: str = os.path.expanduser("~/.ssh/bitssh_passwords.json")


def _load() -> dict:
    if not os.path.exists(PASSWORD_FILE_PATH):
        return {}
    with open(PASSWORD_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return {}
    return json.loads(content)


def _save(data: dict) -> None:
    ssh_dir = os.path.dirname(PASSWORD_FILE_PATH)
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir, mode=0o700, exist_ok=True)

    with open(PASSWORD_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.chmod(PASSWORD_FILE_PATH, 0o600)


def has_password(host: str) -> bool:
    return host in _load()


def save_password(host: str, password: str) -> None:
    """Encrypt `password` with a device-bound key and store it for `host`."""
    data = _load()
    data[host] = crypto.encrypt(password)
    _save(data)


def get_password(host: str) -> Optional[str]:
    """Return the decrypted password for `host`, or None if not stored.

    Raises crypto.DecryptionError if an entry exists but cannot be decrypted
    on this device (e.g. the password file was copied from another machine).
    """
    data = _load()
    entry = data.get(host)
    if entry is None:
        return None
    return crypto.decrypt(entry)


def delete_password(host: str) -> None:
    """Remove the stored password for `host`, if any. No-op if absent."""
    data = _load()
    if host in data:
        del data[host]
        _save(data)
