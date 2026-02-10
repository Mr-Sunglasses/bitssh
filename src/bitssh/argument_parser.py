from argparse import ArgumentParser, Namespace
from typing import Optional


class Config:
    def __init__(self) -> None:
        parser: ArgumentParser = ArgumentParser(
            description="A New and Modern SSH connector written in Python."
        )
        parser.add_argument(
            "--version",
            "-v",
            action="store_true",
            default=False,
            help="Show the bitssh version.",
        )

        # Subcommands
        subparsers = parser.add_subparsers(dest="command")

        # `bitssh add` subcommand
        add_parser = subparsers.add_parser(
            "add", help="Add a new host to the SSH config file."
        )
        add_parser.add_argument(
            "--host",
            type=str,
            default=None,
            help="The alias/name for the SSH host (e.g. myserver).",
        )
        add_parser.add_argument(
            "--hostname",
            type=str,
            default=None,
            help="The hostname or IP address of the server (e.g. 192.168.1.1).",
        )
        add_parser.add_argument(
            "--user",
            type=str,
            default=None,
            help="The username to connect as (e.g. root).",
        )
        add_parser.add_argument(
            "--port",
            type=int,
            default=None,
            help="The port number for SSH (default: 22).",
        )
        add_parser.add_argument(
            "--identity-file",
            type=str,
            default=None,
            help="Path to the private key file (e.g. ~/.ssh/id_rsa).",
        )

        args: Namespace = parser.parse_args()
        self.version: bool = args.version
        self.command: Optional[str] = args.command

        # Add-specific attributes
        self.host: Optional[str] = getattr(args, "host", None)
        self.hostname: Optional[str] = getattr(args, "hostname", None)
        self.user: Optional[str] = getattr(args, "user", None)
        self.port: Optional[int] = getattr(args, "port", None)
        self.identity_file: Optional[str] = getattr(args, "identity_file", None)

    def is_add_interactive(self) -> bool:
        """Return True if `bitssh add` was called without any flags (interactive mode)."""
        return self.command == "add" and all(
            v is None for v in [self.host, self.hostname, self.user, self.port, self.identity_file]
        )

    def is_add_non_interactive(self) -> bool:
        """Return True if `bitssh add` was called with at least --host and --hostname."""
        return (
            self.command == "add"
            and self.host is not None
            and self.hostname is not None
        )
