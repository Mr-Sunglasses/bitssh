from bitssh import __version__

from .argument_parser import Config
from .prompt import add_host_prompt, ask_host_prompt
from .ui import console, draw_table
from .utils import write_host_to_config


def _handle_add(config: Config) -> None:
    """Handle the `bitssh add` subcommand."""
    if config.is_add_interactive():
        # Interactive mode: no flags provided, launch InquirerPy prompts
        add_host_prompt()
    elif config.is_add_non_interactive():
        # Non-interactive mode: --host and --hostname provided (minimum required)
        try:
            write_host_to_config(
                host=config.host,
                hostname=config.hostname,
                user=config.user,
                port=config.port,
                identity_file=config.identity_file,
            )
            console.print(
                f"[bold green]Success![/bold green] Host '[cyan]{config.host}[/cyan]' "
                f"has been added to the SSH config. 🎉",
            )
        except ValueError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
    else:
        # Partial flags: --host and --hostname are both required for non-interactive
        console.print(
            "[bold red]Error:[/bold red] Non-interactive mode requires at least "
            "[cyan]--host[/cyan] and [cyan]--hostname[/cyan] flags.\n"
        )
        console.print("Usage examples:")
        console.print(
            "  [green]bitssh add[/green]                                         "
            "# Interactive mode"
        )
        console.print(
            "  [green]bitssh add --host myserver --hostname 192.168.1.1[/green]  "
            "# Non-interactive mode"
        )
        console.print(
            "  [green]bitssh add --host myserver --hostname 192.168.1.1 "
            "--user root --port 2222[/green]"
        )


def run():
    try:
        config = Config()
        if config.version:
            print(f"bitssh {__version__}")
        elif config.command == "add":
            _handle_add(config)
        else:
            draw_table()
            ask_host_prompt()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error Happed {e}")
