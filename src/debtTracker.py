import argparse
import pathlib
from typing import List, Optional

from commentAggregator import commentAggregator
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
            help="Path to the repo which should be scanned for tech-debt",
        )

        args_group.add_argument(
            "--search_area",
            "-s",
            nargs="+",
            type=pathlib.Path,
            help="One or more repo paths which aggregated summaries should be shown for",
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
        repo_path = self.args.repo_path.resolve()

        # Get all filepaths we are extracting comments from
        scanner = fileScanner(repo_path)
        file_paths = scanner.run()

        # Parse out comments into ParsedComment instances
        parser = fileParser(file_paths)
        parsed_comments = parser.run()

        # Pass comments to aggregator class
        aggregator = commentAggregator(parsed_comments)

        # Aggregated summary of comments within each file
        file_groups = aggregator.aggregate_by_file()

        #  Print for debug purposes
        for group in file_groups:
            print(group)

    def main(self):
        """Execute the app"""
        self.run()


if __name__ == "__main__":
    tracker = DebtTracker.from_cli()
    tracker.main()
