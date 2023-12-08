import os
from .prompt import Prompt
from .ui import UI
from .argument_parser import Config
from bitssh import __version__


def main():
    config = Config()
    if config.version:
        print(f"bitssh {__version__}")
    else:
        UI.draw_table()
        Prompt.ask_host_prompt()


if __name__ == "__main__":
    main()
