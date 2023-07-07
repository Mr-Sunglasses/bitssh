import os
import re

def get_config_path():
    try:
        config_path = os.path.expanduser("~/.ssh/config")
        return config_path
    except FileNotFoundError:
        raise f"Config File Not Found"


def get_config_content(config_file):
    config = {}
    current_host = None

    with open(config_file, "r") as f:
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