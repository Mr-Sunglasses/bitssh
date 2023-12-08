import inquirer
from inquirer.themes import GreenPassion
from .utils import ConfigPathUtility
from .ui import UI
import os


class Prompt:
    @classmethod
    def ask_host_prompt(cls):
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
        UI.console.print(
            "Please Wait While Your System is Connecting to the Remote Server",
            style="green",
        )
        os.system(cmd)
