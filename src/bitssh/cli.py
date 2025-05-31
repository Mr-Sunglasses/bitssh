from bitssh import __version__

from .argument_parser import Config
from .prompt import ask_host_prompt
from .ui import draw_table


def run():
    try:
        config = Config()
        if config.version:
            print(f"bitssh {__version__}")
        else:
            draw_table()
            ask_host_prompt()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error Happed {e}")
