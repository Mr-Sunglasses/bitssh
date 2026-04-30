import os
import subprocess
from typing import List

from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from rich.table import Table

from .ui import console
from .utils import (
    get_config_content,
    get_config_file_host_data,
    host_exists,
    remove_host_from_config,
    write_host_to_config,
)


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


def _validate_host_alias(alias: str) -> bool:
    """Validate that the host alias is not empty and doesn't already exist."""
    if not alias or not alias.strip():
        return False
    return True


def add_host_prompt() -> None:
    """Interactive prompt to collect SSH host details and add to config."""
    console.print(
        "\n[bold cyan]Add a New SSH Host[/bold cyan] 🖥️\n",
    )

    try:
        host = inquirer.text(
            message="Host (alias for the connection):",
            validate=lambda val: len(val.strip()) > 0,
            invalid_message="Host alias cannot be empty.",
        ).execute()

        if host_exists(host.strip()):
            console.print(
                "[bold red]Error:[/bold red] Host "
                f"'{host.strip()}' already exists in the SSH config.",
            )
            return

        hostname = inquirer.text(
            message="HostName (IP address or domain):",
            validate=lambda val: len(val.strip()) > 0,
            invalid_message="HostName cannot be empty.",
        ).execute()

        user = inquirer.text(
            message="User (login username, leave empty to skip):",
            default="",
        ).execute()

        port = inquirer.text(
            message="Port (default: 22):",
            default="22",
            validate=NumberValidator(message="Port must be a number."),
        ).execute()

        identity_file = inquirer.text(
            message="IdentityFile (path to private key, leave empty to skip):",
            default="",
        ).execute()

        # Normalize values
        host = host.strip()
        hostname = hostname.strip()
        user = user.strip() if user.strip() else None
        port_int = int(port) if port.strip() else None
        identity_file = identity_file.strip() if identity_file.strip() else None

        # Show summary before writing
        console.print("\n[bold yellow]Summary:[/bold yellow]")
        console.print(f"  Host:          [cyan]{host}[/cyan]")
        console.print(f"  HostName:      [cyan]{hostname}[/cyan]")
        if user:
            console.print(f"  User:          [cyan]{user}[/cyan]")
        if port_int and port_int != 22:
            console.print(f"  Port:          [cyan]{port_int}[/cyan]")
        else:
            console.print("  Port:          [cyan]22[/cyan]")
        if identity_file:
            console.print(f"  IdentityFile:  [cyan]{identity_file}[/cyan]")

        confirm = inquirer.confirm(
            message="Add this host to SSH config?",
            default=True,
        ).execute()

        if not confirm:
            console.print("[yellow]Cancelled.[/yellow] No changes were made.")
            return

        write_host_to_config(
            host=host,
            hostname=hostname,
            user=user,
            port=port_int,
            identity_file=identity_file,
        )

        console.print(
            "[bold green]Success![/bold green] Host "
            f"'[cyan]{host}[/cyan]' has been added to the SSH config. 🎉",
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
    except ValueError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}")


def remove_host_prompt() -> None:
    """Interactive prompt to select and remove an SSH host from config."""
    try:
        hosts = get_config_file_host_data()
        if not hosts:
            console.print("[bold yellow]No hosts found in SSH config.[/bold yellow]")
            return

        selected = inquirer.fuzzy(
            message="Select the host to remove:",
            choices=hosts,
        ).execute()

        if selected is None:
            return

        try:
            host_alias = selected.split("-> ")[1].strip()
        except IndexError:
            raise ValueError("Invalid format: expected '-> ' delimiter in the answer.")

        host_info = get_config_content().get(host_alias, {})

        table = Table(title=f"Removing Host: {host_alias}")
        table.add_column("Property", style="bold cyan", justify="left")
        table.add_column("Value", style="magenta", justify="left")
        table.add_row("Host", host_alias)
        table.add_row("HostName", host_info.get("Hostname", "N/A"))
        table.add_row("User", host_info.get("User", "N/A"))
        table.add_row("Port", host_info.get("Port", "22"))
        console.print(table)

        confirm = inquirer.confirm(
            message=f"Remove host '{host_alias}' from SSH config?",
            default=False,
        ).execute()

        if not confirm:
            console.print("[yellow]Cancelled.[/yellow] No changes were made.")
            return

        remove_host_from_config(host_alias)
        console.print(
            f"[bold green]Success![/bold green] Host '[cyan]{host_alias}[/cyan]' "
            f"has been removed from the SSH config. 🗑️",
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
    except ValueError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}")
