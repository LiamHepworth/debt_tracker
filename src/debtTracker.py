import argparse
import pathlib
from typing import List, Optional

from fileParser import fileParser
from fileScanner import fileScanner


class DebtTracker:

    @classmethod
    def build_parser(cls):
        """
        Create an argument parser to receive input from the command line
        """
        parser = argparse.ArgumentParser(prog=cls.__name__)

        args_group = parser.add_argument_group("group")

        args_group.add_argument(
            "--repo_path",
            "-p",
            required=True,
            type=pathlib.Path,
            help="Path to the repo which should be scanned",
        )

        return parser

    @classmethod
    def from_cli(cls, argv: Optional[List[str]] = None):
        """
        Gets command line args using argparse, making them available to the class.
        """
        args = cls.build_parser().parse_args(argv)
        return cls(args)

    def __init__(self, args):
        """Initialize the app."""
        self.args = args

    def run(self):
        """Entry point"""
        scanner = fileScanner(self.args.repo_path)
        file_paths = scanner.run()

        parser = fileParser(file_paths)
        print(parser.run())

    def main(self):
        """Execute the app"""
        self.run()


if __name__ == "__main__":
    tracker = DebtTracker.from_cli()
    tracker.main()
