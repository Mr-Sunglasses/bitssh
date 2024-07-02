import os
from .prompt import ask_host_prompt
from .ui import draw_table
from .argument_parser import Config
from bitssh import __version__


def run():
    config = Config()
    if config.version:
        print(f"bitssh {__version__}")
    else:
        draw_table()
        ask_host_prompt()
