import inquirer
from inquirer.themes import GreenPassion
from .utils import ConfigPathUtility
from .ui import console
import os
from inquirer import List
from typing import List, Dict, Optional


def ask_host_prompt():
    HOST: List[str] = ConfigPathUtility.get_config_file_host_data()
    questions: List[List] = [
        inquirer.List(
            name="host",
            message="Select the Host Given in the Above List",
            choices=HOST,
        ),
    ]
    try:
        answers: Optional[Dict[str, str]] = inquirer.prompt(
            questions=questions, theme=GreenPassion()
        )
        if answers is None:
            return

        cmd: str = answers["host"]
        cmd = cmd[6:]
        cmd = f"ssh {cmd}"
        console.print(
            "Please Wait While Your System is Connecting to the Remote Server 🖥️",
            style="green",
        )
        os.system(cmd)
    except Exception as Error:
        print(f"\nInterrupted by {Error}")
