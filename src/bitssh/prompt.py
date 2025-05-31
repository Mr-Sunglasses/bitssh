import os
from typing import Dict, List, Optional

from InquirerPy import inquirer

from .ui import console
from .utils import get_config_file_host_data

def ask_host_prompt():
    HOST: List[str] = get_config_file_host_data()
    questions: List[List] = inquirer.fuzzy(
        message="Select the Host Given in the Above List: ",
        choices=HOST,
    )
    try:
        answers: Optional[Dict[str, str]] = questions.execute()
        if answers is None:
            return

        cmd: str = answers
        cmd = cmd[7::]
        cmd = f"ssh {cmd}"
        os.system("cls" if os.name == "nt" else "clear")
        console.print(
            "Please Wait While Your System is Connecting to the Remote Server 🖥️",
            style="green",
        )
        os.system(cmd)
    except Exception as Error:
        print(f"\nInterrupted by {Error}")
