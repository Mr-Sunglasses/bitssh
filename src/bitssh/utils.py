import os
import re
from typing import Dict, List, Tuple

CONFIG_FILE_PATH: str = os.path.expanduser("~/.ssh/config")


def _validate_config_file() -> None:
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_FILE_PATH}. "
            "Please see the documentation for bitssh."
        )


def get_config_content() -> Dict[str, Dict[str, str]]:
    _validate_config_file()

    with open(CONFIG_FILE_PATH, "r") as file:
        lines = file.read()

    host_pattern = re.compile(r"Host\s+(\w+)", re.MULTILINE)
    hostname_pattern = re.compile(r"(?:HostName|Hostname)\s+(\S+)", re.MULTILINE)
    user_pattern = re.compile(r"User\s+(\S+)", re.MULTILINE)

    host_dict: Dict[str, Dict[str, str]] = {}
    for match in host_pattern.finditer(lines):
        host = match.group(1)
        host_end = match.end()

        hostname_match = hostname_pattern.search(lines, host_end)
        hostname = hostname_match.group(1) if hostname_match else host

        user_match = user_pattern.search(lines, host_end)
        user = user_match.group(1) if user_match else None

        host_dict[host] = {
            "Hostname": hostname,
            "User": user,
        }

    return host_dict


def get_config_file_row_data() -> List[Tuple[str, str, str, str]]:
    config_content = get_config_content()
    rows = []
    for host, attributes in config_content.items():
        hostname = attributes["Hostname"]
        user = attributes["User"]
        rows.append((hostname, host, "22", user))
    return rows


def get_config_file_host_data() -> List[str]:
    return [f"🖥️  -> {row[1]}" for row in get_config_file_row_data()]
