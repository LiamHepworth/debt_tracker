from pathlib import Path
from typing import Iterable, List, Set


class fileScanner:
    """
    Class which walks through one or more repo paths,
    and extracts paths to each file.
    """

    def __init__(self, repo_paths: Iterable[Path]):
        """Initialize the scanner with the repo paths to inspect."""

        # List comprehension to get all absolute paths
        self.repo_paths = [Path(repo_path).resolve() for repo_path in repo_paths]

    def run(self) -> List[str]:
        """Return absolute paths for all files inside the target directories."""

        # Set to hold all file paths without duplicates
        file_paths: Set[str] = set()

        for repo_path in self.repo_paths:
            # Get all sub-paths in the directory
            for path in repo_path.rglob("*"):
                # Filter for only files (not dirs), and add to list.
                if path.is_file():
                    file_paths.add(str(path.resolve()))

        # Return filepaths as a list
        return sorted(file_paths)

    def main(self) -> List[str]:
        """Execute the app."""
        return self.run()
