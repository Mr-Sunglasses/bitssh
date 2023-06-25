from rich.panel import Panel
import os
from rich.console import Console
from rich.table import Table
import inquirer
from inquirer.themes import GreenPassion
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

    with open(config_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if re.match(r'^Host\s+', line):
            current_host = re.sub(r'^Host\s+', '', line)
            config[current_host] = {}
        else:
            match = re.match(r'^\s*([\w-]+)\s+(.*)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                config[current_host][key] = value

    return config


try:
    content = get_config_content(config_file=get_config_path())
except FileNotFoundError:
    print("Config file is not Found in ~/.ssh/config")
ROWS = [
]

for host, attributes in content.items():
    row = (attributes['Hostname'], host,
           attributes['port'], attributes['User'])
    ROWS.append(row)


table = Table(title="SSH Servers in Config File")

table.add_column("Hostname", justify="left", style="cyan", no_wrap=True)
table.add_column("Host", style="magenta")
table.add_column("Port", justify="right", style="green")
table.add_column("User", justify="right", style="yellow")

for i in ROWS:
    table.add_row(i[0], i[1], i[2], i[3])


console = Console()
console.print(table)

HOST = []

for hosts in ROWS:
    HOST.append(f"Host: {hosts[1]}")


questions = [
    inquirer.List(
        name="host",
        message="Select the Host Given in the Above List",
        choices=HOST
    ),
]


def main():
    answers = inquirer.prompt(questions=questions, theme=GreenPassion())
    cmd = answers['host']
    cmd = cmd[6::]
    cmd = f"ssh {cmd}"
    console.print(
        "Please Wait While Your System is Connecting to the Remote Server", style="green")
    os.system(cmd)
