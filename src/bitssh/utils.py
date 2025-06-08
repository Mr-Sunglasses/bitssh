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


def get_config_content():
    _validate_config_file()
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        lines = file.read()

    # Remove commented lines and empty lines
    filtered_lines = []
    for line in lines.split("\n"):
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("#"):
            filtered_lines.append(line)

    filtered_content = "\n".join(filtered_lines)

    # Case-insensitive patterns - make sure all are properly case-insensitive
    # Fixed: Use \S+ instead of \w+ to match non-whitespace characters (includes hyphens, dots, etc.)
    host_pattern = re.compile(r"^Host\s+(\S+)", re.MULTILINE | re.IGNORECASE)
    hostname_pattern = re.compile(
        r"^\s*(?:HostName|Hostname)\s+(\S+)", re.MULTILINE | re.IGNORECASE
    )
    user_pattern = re.compile(r"^\s*User\s+(\S+)", re.MULTILINE | re.IGNORECASE)
    port_pattern = re.compile(r"^\s*port\s+(\d+)", re.MULTILINE | re.IGNORECASE)

    host_dict = {}

    # Find all host matches first
    host_matches = list(host_pattern.finditer(filtered_content))

    for i, match in enumerate(host_matches):
        host = match.group(1)

        # Find the end of this host section (start of next host or end of content)
        if i + 1 < len(host_matches):
            host_section_end = host_matches[i + 1].start()
        else:
            host_section_end = len(filtered_content)

        # Extract only this host's section (from end of Host line to start of next Host)
        host_section = filtered_content[match.end() : host_section_end]

        # Search within this host section only
        hostname_match = hostname_pattern.search(host_section)
        hostname = hostname_match.group(1) if hostname_match else host

        user_match = user_pattern.search(host_section)
        user = user_match.group(1) if user_match else None

        port_match = port_pattern.search(host_section)
        port = port_match.group(1) if port_match else "22"

        host_dict[host] = {
            "Hostname": hostname,
            "User": user,
            "Port": port,
        }

    return host_dict


def get_config_file_row_data():
    config_content = get_config_content()
    rows = []
    for host, attributes in config_content.items():
        hostname = attributes["Hostname"]
        user = attributes["User"]
        port = attributes["Port"]
        rows.append((hostname, host, port, user))
    return rows


def get_config_file_host_data() -> List[str]:
    return [f"🖥️  -> {row[1]}" for row in get_config_file_row_data()]
