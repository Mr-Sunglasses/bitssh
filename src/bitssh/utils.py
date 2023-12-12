import os
import re


class ConfigPathUtility:
    config_file_path = os.path.expanduser("~/.ssh/config")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            "Config file is not Found in ~/.ssh/config Please See the Docs of bitssh."
        )

    @classmethod
    def get_config_content(cls):

        with open(cls.config_file_path, "r") as f:
            lines = f.read()

        host_pattern = re.compile(r"Host\s+(\w+)", re.MULTILINE)
        hostname_pattern = re.compile(
            r"(?:HostName|Hostname)\s+(\S+)", re.MULTILINE)
        user_pattern = re.compile(r"User\s+(\S+)", re.MULTILINE)
        host_dict = {}
        for match in host_pattern.finditer(lines):
            host = match.group(1)
            hostname_match = hostname_pattern.search(lines, match.end())
            if hostname_match:
                hostname = hostname_match.group(1)
            else:
                hostname = host
            user = user_pattern.search(lines, match.end())
            if user:
                user = user.group(1)
            host_dict[host] = {
                "Hostname": hostname,
                "User": user,
            }

        return host_dict

    @classmethod
    def get_config_file_row_data(cls):
        config_content = cls.get_config_content()

        ROWS = []

        for host, attributes in config_content.items():
            row = (attributes["Hostname"], host,
                   '22', attributes["User"])
            ROWS.append(row)

        return ROWS

    @classmethod
    def get_config_file_host_data(cls):
        HOST = []
        for hosts in cls.get_config_file_row_data():
            HOST.append(f"🖥️  -> {hosts[1]}")
        return HOST
