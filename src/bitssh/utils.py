import os
import re

from path import Path
from typing import Dict, Pattern, Optional, Match, List, Tuple


class ConfigPathUtility:
    config_file_path: Path = os.path.expanduser("~/.ssh/config")

    @classmethod
    def _validate_config_file(cls) -> None:
        if not os.path.exists(cls.config_file_path):
            raise FileNotFoundError(
                f"Config file not found at {cls.config_file_path}. Please see the documentation for bitssh."
            )

    @classmethod
    def get_config_content(cls) -> Dict[str, Dict[str, str]]:
        cls._validate_config_file()

        with open(cls.config_file_path, "r") as file:
            lines = file.read()

        host_pattern: Pattern[str] = re.compile(r"Host\s+(\w+)", re.MULTILINE)
        hostname_pattern: Pattern[str] = re.compile(r"(?:HostName|Hostname)\s+(\S+)", re.MULTILINE)
        user_pattern: Pattern[str] = re.compile(r"User\s+(\S+)", re.MULTILINE)

        host_dict: Dict[str, Dict[str, str]] = {}
        for match in host_pattern.finditer(lines):
            host: str = match.group(1)
            hostname_match: Optional[Match[str]] = hostname_pattern.search(lines, match.end())
            hostname: str = hostname_match.group(1) if hostname_match else host

            user_match: Optional[Match[str]] = user_pattern.search(lines, match.end())
            user: Optional[str] = user_match.group(1) if user_match else None

            host_dict[host]: Dict[str, str] = {
                "Hostname": hostname,
                "User": user,
            }

        return host_dict

    @classmethod
    def get_config_file_row_data(cls) -> List[Tuple[str, str, str, str]]:
        config_content = cls.get_config_content()

        rows: List[Tuple[str, str, str, str]] = [
            (attributes["Hostname"], host, "22", attributes["User"])
            for host, attributes in config_content.items()
        ]

        return rows

    @classmethod
    def get_config_file_host_data(cls) -> List[str]:
        return [f"🖥️  -> {host[1]}" for host in cls.get_config_file_row_data()]
