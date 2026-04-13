import re
from pathlib import Path
from typing import List, NamedTuple, Pattern, Sequence


class ParsedComment(NamedTuple):
    """
    Data structure to hold a matched comment marker in a file.
    """

    file_path: str
    line_number: int
    keyword: str
    line_content: str


class fileParser:
    """
    Class to parse tracked files and extract comment-like markers.
    """

    DEFAULT_KEYWORDS = ("FIX", "NOTE", "TODO", "REVISIT", "BUG")

    def __init__(
        self,
        file_paths: Sequence[str],
        keywords: Sequence[str] | None = None,
    ):
        """Initialize the parser with files to inspect and keywords to match."""
        # Array of Path objects pointing to each file
        self.file_paths = [Path(file_path) for file_path in file_paths]

        # Use custom keywords when provided, otherwise fall back to the defaults.
        if keywords:
            self.keywords = tuple(keyword.upper() for keyword in keywords)
        else:
            self.keywords = self.DEFAULT_KEYWORDS

        # Regex pattern to match keywords
        self.pattern = self._build_pattern(self.keywords)

    def _build_pattern(self, keywords: Sequence[str]) -> Pattern[str]:
        """Create a regex pattern to match keywords."""

        # Escape the keywords, ensuring special characters are handled
        escaped_keywords = []

        for keyword in keywords:
            escaped_keywords.append(re.escape(keyword))

        # Join the escaped keywords into a pipe-separated string
        keyword_pattern = "|".join(escaped_keywords)

        # Create a the full regex pattern and compile it for reusability
        final_pattern = r"\b(" + keyword_pattern + r")\b"
        return re.compile(final_pattern, re.IGNORECASE)

    def _parse_file(self, file_path: Path) -> List[ParsedComment]:
        """Extract all configured markers from a single file."""
        # List to hold parsed comment instances
        parsed_comments: List[ParsedComment] = []

        # Try to open the file, return OSError if it doesn't work
        try:
            # Open the file and loop through each line
            with file_path.open("r", encoding="utf-8", errors="ignore") as file_handle:
                for line_number, line in enumerate(file_handle, start=1):

                    # Find all regex matches for a keyword within a single line in the file
                    matches = self.pattern.finditer(line)

                    # Loop through the matches,
                    # and create a new ParsedComment instance to hold each one
                    for match in matches:
                        parsed_comments.append(
                            ParsedComment(
                                file_path=str(file_path.resolve()),
                                line_number=line_number,
                                keyword=match.group(1).upper(),
                                line_content=line.rstrip(),
                            )
                        )
        except OSError:
            return []

        # Return the parsed comments
        return parsed_comments

    def run(self) -> List[ParsedComment]:
        """Parse all files and return any matched comment markers."""

        # List to hold all instances of parsed comments
        all_parsed_comments: List[ParsedComment] = []

        # Extend the list (rather than append, to keep it flat)
        for file_path in self.file_paths:
            all_parsed_comments.extend(self._parse_file(file_path))

        # Return the list
        return all_parsed_comments

    def main(self) -> List[ParsedComment]:
        """Execute the app."""
        return self.run()
