import os
import re
import pprint

class ConfigPathUtility:

    config_file_path = os.path.expanduser("~/.ssh/config")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError("Config file is not Found in ~/.ssh/config Please See the Docs of bitssh.")
    @classmethod
    def get_config_content(cls):
        config = {}
        current_host = None

        with open(cls.config_file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            if re.match(r"^Host\s+", line):
                current_host = re.sub(r"^Host\s+", "", line)
                config[current_host] = {}
            else:
                match = re.match(r"^\s*([\w-]+)\s+(.*)", line)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    config[current_host][key] = value

        return config

    @classmethod
    def get_config_file_row_data(cls):
        config_content = cls.get_config_content()

        ROWS = []

        for host, attributes in config_content.items():
            row = (attributes["Hostname"], host,
                   attributes["port"], attributes["User"])
            ROWS.append(row)

        return ROWS

    @classmethod
    def get_config_file_host_data(cls):
        HOST = []
        for hosts in cls.get_config_file_row_data():
            HOST.append(f"Host: {hosts[1]}")
        return HOST