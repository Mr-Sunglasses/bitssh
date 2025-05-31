import os
import subprocess
from typing import Dict, List, Optional

from InquirerPy import inquirer

from .ui import console
from .utils import get_config_file_host_data


def ask_host_prompt():
    HOST: List[str] = get_config_file_host_data()
    questions = inquirer.fuzzy(
        message="Select the Host Given in the Above List: ",
        choices=HOST,
    )
    try:
        answers = questions.execute()
        if answers is None:
            return

        cmd: str = answers
        try:
            _cmd_exec_data = cmd.split("-> ")[1]  # clean the data from answers
        except IndexError:
            raise ValueError("Invalid format: expected '-> ' delimiter in the answer.")
        if os.name == "nt":  # Windows
            subprocess.run(["cls"], shell=True, check=True)
        else:  # Unix-like systems
            subprocess.run(["clear"], check=True)
        console.print(
            "Please Wait While Your System is Connecting to the Remote Server 🖥️",
            style="green",
        )
        subprocess.run(["ssh", _cmd_exec_data], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stdout}")
    except Exception as Error:
        print(f"\nInterrupted by {Error}")
