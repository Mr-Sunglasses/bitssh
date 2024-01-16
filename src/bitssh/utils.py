import os
import re

from path import Path
from typing import Dict, Pattern, Optional, Match, List, Tuple


class ConfigPathUtility:
    config_file_path: Path = Path(os.path.expanduser("~/.ssh/config"))
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            "Config file is not Found in ~/.ssh/config Please See the Docs of bitssh."
        )

    @classmethod
    def get_config_content(cls) -> Dict[str, Dict[str, str]]:
        with open(cls.config_file_path, "r") as f:
            lines = f.read()

        host_pattern: Pattern[str] = re.compile(r"Host\s+(\w+)", re.MULTILINE)
        hostname_pattern: Pattern[str] = re.compile(
            r"(?:HostName|Hostname)\s+(\S+)", re.MULTILINE
        )
        user_pattern: Pattern[str] = re.compile(r"User\s+(\S+)", re.MULTILINE)
        host_dict: Dict[str, Dict[str, str]] = {}

        for match in host_pattern.finditer(lines):
            host: str = match.group(1)
            hostname_match: Optional[Match[str]] = hostname_pattern.search(
                lines, match.end()
            )
            if hostname_match:
                hostname: str = hostname_match.group(1)
            else:
                hostname: str = host
            user: Optional[Match[str]] = user_pattern.search(lines, match.end())
            if user:
                user: str = user.group(1)
            host_dict[host] = {
                "Hostname": hostname,
                "User": user,
            }

        return host_dict

    @classmethod
    def get_config_file_row_data(cls) -> List[Tuple[str, str, str, str]]:
        config_content = cls.get_config_content()

        ROWS: List[Tuple[str, str, str, str]] = []

        for host, attributes in config_content.items():
            row: Tuple[str, str, str, str] = (
                attributes["Hostname"],
                host,
                "22",
                attributes["User"],
            )
            ROWS.append(row)

        return ROWS

    @classmethod
    def get_config_file_host_data(cls) -> List[str]:
        HOST: List[str] = []
        for hosts in cls.get_config_file_row_data():
            HOST.append(f"🖥️  -> {hosts[1]}")
        return HOST
