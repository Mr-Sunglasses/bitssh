from argparse import ArgumentParser


class Config:
    def __init__(self) -> None:
        parser: ArgumentParser = ArgumentParser(
            description="A New and Modern SSH connector written in Python."
        )
        parser.add_argument(
            "--version",
            action="store_true",
            default=False,
            help="Show the bitssh version.",
        )

        args, _ = parser.parse_known_args()
        self.version = args.version
