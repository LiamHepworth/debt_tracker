from pathlib import Path
from typing import Dict, Iterable, List

from fileParser import ParsedComment


class commentsOfFile:
    """
    Class to hold all instances of comments within a file
    """

    def __init__(self, file_path: str | Path, comments: Iterable[ParsedComment]):

        self.file_path = str(Path(file_path).resolve())

        # Assign comments as a list sorted by line number
        self.comments = sorted(comments, key=lambda comment: (comment.line_number))

    @property
    def total_comments(self) -> int:
        """Return the number of matched comments inside the file."""
        return len(self.comments)

    def keyword_counts(self) -> Dict[str, int]:
        """Return a count of matched keywords for this file."""
        counts: Dict[str, int] = {}

        for comment in self.comments:
            counts[comment.keyword] = counts.get(comment.keyword, 0) + 1

        return counts


class commentsOfArea:
    """
    Class to hold all instances of comments within a user-specified directory area.
    """

    def __init__(self, area_path: str | Path, comments: Iterable[ParsedComment]):

        # Resolve the path to make it absolute, and convert to string
        self.area_path = str(Path(area_path).resolve())

        # Assign comments as a list sorted by file path and line number
        self.comments = sorted(
            comments, key=lambda comment: (comment.file_path, comment.line_number)
        )

    @property
    def total_comments(self) -> int:
        """Return the number of matched comments inside the area."""
        return len(self.comments)

    def keyword_counts(self) -> Dict[str, int]:
        """Return a count of matched keywords for this area."""
        counts: Dict[str, int] = {}

        for comment in self.comments:
            counts[comment.keyword] = counts.get(comment.keyword, 0) + 1

        return counts


class commentAggregator:
    """
    Class to sort comments by aggregation method
    """

    def __init__(self, comments: Iterable[ParsedComment]):

        # Store parsed comments as a list on this class
        self.comments = list(comments)

    def aggregate_by_file(self) -> List[commentsOfFile]:
        """Group parsed comments by their source file."""

        # Dict to hold comments grouped by file
        grouped_comments: Dict[str, List[ParsedComment]] = {}

        for comment in self.comments:

            # Create a new dict entry for the file path
            if comment.file_path not in grouped_comments:
                grouped_comments[comment.file_path] = []

            # Append the comment to the list value for the file path
            grouped_comments[comment.file_path].append(comment)

        # Convert dict to a list of structured objects,
        # Allows for easier processing / operation downstream
        file_groups: List[commentsOfFile] = []

        for file_path in sorted(grouped_comments.keys()):
            file_group = commentsOfFile(file_path, grouped_comments[file_path])
            file_groups.append(file_group)

        return file_groups

    def aggregate_by_area(
        self, search_areas: Iterable[str | Path]
    ) -> List[commentsOfArea]:
        """
        Aggregates comments by the specified search areas.
        """

        # Dict to hold paths and comment list
        grouped_comments: Dict[str, List[ParsedComment]] = {}

        # List of absolute search paths
        resolved_areas = [Path(area_path).resolve() for area_path in search_areas]

        # Create a new key in the dict for each search area
        # Instatiate and empty list as a default value
        for area_path in resolved_areas:
            grouped_comments[str(area_path)] = []

        for comment in self.comments:
            comment_path = Path(comment.file_path).resolve()

            for area_path in resolved_areas:
                # If the comment path matches the area path or if the comment path is within the area path
                if comment_path == area_path or area_path in comment_path.parents:
                    # Then append the comment as a value in the dict
                    grouped_comments[str(area_path)].append(comment)

        # Convert dict to a list of objects:
        area_groups: List[commentsOfArea] = []

        for area_path in sorted(grouped_comments.keys()):
            if grouped_comments[area_path]:
                area_group = commentsOfArea(area_path, grouped_comments[area_path])
                area_groups.append(area_group)

        return area_groups

    def all_keyword_counts(self) -> Dict[str, int]:
        """Return total matched keyword counts across all files."""
        counts: Dict[str, int] = {}

        # Consolidate all the individual keyword counts per file into one object
        for file_group in self.aggregate_by_file():
            for keyword, count in file_group.keyword_counts().items():
                counts[keyword] = counts.get(keyword, 0) + count

        return counts
