import os
import re


class ConfigPathUtility:
    config_file_path = os.path.expanduser("~/.ssh/config")

    @classmethod
    def _validate_config_file(cls):
        if not os.path.exists(cls.config_file_path):
            raise FileNotFoundError(
                f"Config file not found at {cls.config_file_path}. Please see the documentation for bitssh."
            )

    @classmethod
    def get_config_content(cls):
        cls._validate_config_file()

        with open(cls.config_file_path, "r") as file:
            lines = file.read()

        host_pattern = re.compile(r"Host\s+(\w+)", re.MULTILINE)
        hostname_pattern = re.compile(r"(?:HostName|Hostname)\s+(\S+)", re.MULTILINE)
        user_pattern = re.compile(r"User\s+(\S+)", re.MULTILINE)

        host_dict = {}
        for match in host_pattern.finditer(lines):
            host = match.group(1)
            hostname_match = hostname_pattern.search(lines, match.end())
            hostname = hostname_match.group(1) if hostname_match else host

            user_match = user_pattern.search(lines, match.end())
            user = user_match.group(1) if user_match else None

            host_dict[host] = {
                "Hostname": hostname,
                "User": user,
            }

        return host_dict

    @classmethod
    def get_config_file_row_data(cls):
        config_content = cls.get_config_content()

        rows = [
            (attributes["Hostname"], host, "22", attributes["User"])
            for host, attributes in config_content.items()
        ]

        return rows

    @classmethod
    def get_config_file_host_data(cls):
        return [f"🖥️  -> {host[1]}" for host in cls.get_config_file_row_data()]
