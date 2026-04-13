import argparse
import pathlib
from typing import List, Optional

from commentAggregator import commentAggregator
from fileParser import fileParser
from fileScanner import fileScanner
from reportRenderer import ReportRenderer


class DebtTracker:

    @classmethod
    def build_parser(cls):
        """
        Create an argument parser to receive input from the command line
        """
        parser = argparse.ArgumentParser(prog=cls.__name__)

        args_group = parser.add_argument_group("group")

        args_group.add_argument(
            "--search_area",
            "-s",
            required=True,
            nargs="+",
            type=pathlib.Path,
            help="One or more repo paths which should be scanned",
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
        search_areas = [search_area.resolve() for search_area in self.args.search_area]

        # Get all filepaths we are extracting comments from
        scanner = fileScanner(search_areas)
        file_paths = scanner.run()

        # Parse out comments into ParsedComment instances
        parser = fileParser(file_paths)
        parsed_comments = parser.run()

        # Pass comments to aggregator class
        aggregator = commentAggregator(parsed_comments)

        # Aggregated summary of comments within a search area
        search_area_comments = aggregator.aggregate_by_area(search_areas)

        # Aggregated summary of comments within each file
        file_aggregates = aggregator.aggregate_by_file()

        # Counts of all the keywords across the entire search area.
        all_keyword_counts = aggregator.all_keyword_counts()

        # Total number of extracted comments in the search area
        total_comments = 0

        for file in file_aggregates:
            total_comments += file.total_comments

        # Total number of files parsed within the search area
        total_files = len(file_paths)

        context = {
            "files": file_aggregates,
            "total_comments": total_comments,
            "total_files": total_files,
        }

        # # Instantiate renderer and render the report to the ./work directory
        renderer = ReportRenderer("./src/templates")
        renderer.render("report_template.html", context, "work/tech_debt_report.html")

        # NOTE:
        # Visualisation hierarchy:
        # Overall summary section - total comments, total files with comments, total areas with comments, summary of keywords, top 10 files with comments?
        # Area level summary - Area Path, total files, total comments, keyword breakdown, this could be a bar chart or table
        # File level summary - table for each file showing keyword, line number, etc etc

    def main(self):
        """Execute the app"""
        self.run()


if __name__ == "__main__":
    tracker = DebtTracker.from_cli()
    tracker.main()
