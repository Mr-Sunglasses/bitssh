import inquirer
from inquirer.themes import GreenPassion
from .utils import ConfigPathUtility
from .ui import console
import os

from inquirer import List
from typing import List, Dict

def ask_host_prompt():
    HOST: list[str] = ConfigPathUtility.get_config_file_host_data()
    questions: list[List] = [
        inquirer.List(
            name="host",
            message="Select the Host Given in the Above List",
            choices=HOST,
        ),
    ]

    answers: Dict[str, str] = inquirer.prompt(questions=questions, theme=GreenPassion())

    cmd: str = answers["host"]
    cmd: str = cmd[6::]
    cmd: str = f"ssh {cmd}"
    console.print(
        "Please Wait While Your System is Connecting to the Remote Server 🖥️",
        style="green",
    )
    os.system(cmd)
