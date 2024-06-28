import inquirer
from inquirer.themes import GreenPassion
from .utils import ConfigPathUtility
from .ui import console
import os


def ask_host_prompt():
    HOST = ConfigPathUtility.get_config_file_host_data()
    questions = [
        inquirer.List(
            name="host",
            message="Select the Host Given in the Above List",
            choices=HOST,
        ),
    ]

    answers = inquirer.prompt(questions=questions, theme=GreenPassion())

    cmd = answers["host"]
    cmd = cmd[6::]
    cmd = f"ssh {cmd}"
    console.print(
        "Please Wait While Your System is Connecting to the Remote Server 🖥️",
        style="green",
    )
    os.system(cmd)
