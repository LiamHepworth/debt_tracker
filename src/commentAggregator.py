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

    def all_keyword_counts(self) -> Dict[str, int]:
        """Return total matched keyword counts across all files."""
        counts: Dict[str, int] = {}

        # Consolidate all the individual keyword counts per file into one object
        for file_group in self.aggregate_by_file():
            for keyword, count in file_group.keyword_counts().items():
                counts[keyword] = counts.get(keyword, 0) + count

        return counts
