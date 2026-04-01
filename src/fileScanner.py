from pathlib import Path
from typing import List


class fileScanner:
    """
    Class which walks through a repo's directory structure,
    and extracts paths to each file.
    """

    def __init__(self, repo_path: Path):
        """Initialize the scanner with the repo path to inspect."""
        self.repo_path = repo_path.resolve()

    def run(self) -> List[str]:
        """Return absolute paths for all files inside the target directory."""

        # List to hold all file paths
        file_paths: List[str] = []

        # Get all sub-paths in the directory
        for path in self.repo_path.rglob("*"):
            # Filter for only files (not dirs), and add to list.
            if path.is_file():
                file_paths.append(str(path.resolve()))

        # Return filepaths as a list
        return file_paths

    def main(self) -> List[str]:
        """Execute the app."""
        return self.run()
