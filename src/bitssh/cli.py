import getpass

from bitssh import __version__  # noqa: F401

from . import password_store
from .argument_parser import Config
from .prompt import add_host_prompt, ask_host_prompt, remove_host_prompt
from .ui import console, draw_table
from .utils import remove_host_from_config, write_host_to_config


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
            if config.ask_password:
                password = getpass.getpass(f"Password for '{config.host}': ")
                if password:
                    password_store.save_password(config.host, password)
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
            "  [green]bitssh add[/green]                                         # Interactive mode"
        )
        console.print(
            "  [green]bitssh add --host myserver --hostname 192.168.1.1[/green]  "
            "# Non-interactive mode"
        )
        console.print(
            "  [green]bitssh add --host myserver --hostname 192.168.1.1 "
            "--user root --port 2222[/green]"
        )


def _handle_remove(config: Config) -> None:
    """Handle the `bitssh remove` subcommand."""
    if config.hosts:
        # Non-interactive mode: --host flag(s) provided
        for host in config.hosts:
            try:
                remove_host_from_config(host)
                password_store.delete_password(host)
                console.print(
                    f"[bold green]Success![/bold green] Host "
                    f"'[cyan]{host}[/cyan]' "
                    f"has been removed from the SSH config. 🗑️",
                )
            except ValueError as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
            except Exception as e:
                console.print(f"[bold red]Unexpected error:[/bold red] {e}")
    else:
        # Interactive mode: launch multiselect prompt
        remove_host_prompt()


def run():
    try:
        config = Config()
        if config.version:
            print(f"bitssh {__version__}")
        elif config.command == "add":
            _handle_add(config)
        elif config.command == "remove":
            _handle_remove(config)
        else:
            draw_table()
            ask_host_prompt()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error Happened: {e}")
