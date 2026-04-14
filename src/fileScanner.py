import json
from pathlib import Path
from typing import Iterable, List, Set


class fileScanner:
    """
    Class which walks through one or more repo paths,
    and extracts paths to each file.
    """

    def __init__(
        self,
        repo_paths: Iterable[Path],
        config_path: str | Path | None = None,
    ):
        """Initialize the scanner with the repo paths to inspect."""

        # List comprehension to get all absolute paths
        self.repo_paths = [Path(repo_path).resolve() for repo_path in repo_paths]

        self.exclude_suffixes = set()
        if config_path is not None:
            self.exclude_suffixes = self.load_exclude_suffixes(config_path)

    @classmethod
    def load_exclude_suffixes(cls, config_path: str | Path) -> Set[str]:
        """Load excluded file suffixes from a JSON config file."""

        # Resolve to an absolute path
        path = Path(config_path).resolve()

        # Read the confg data, handle errors
        try:
            config_data = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise ValueError(f"Unable to read exclude config: {path}") from error

        # Capture all suffixes of files which should be ignored.
        # Using a set to avoid duplicates, converts everything to lowercase too
        suffixes = {
            suffix.lower() for suffix in config_data.get("exclude_suffixes", [])
        }

        return suffixes

    def _is_excluded(self, path: Path) -> bool:
        """Return True when a file path matches a configured suffix."""
        # Capture file suffix, lookup the suffix in the list of excludes
        file_suffix = path.suffix.lower()
        return file_suffix in self.exclude_suffixes

    def run(self) -> List[str]:
        """Return absolute paths for all files inside the target directories."""

        # Set to hold all file paths without duplicates
        file_paths: Set[str] = set()

        for repo_path in self.repo_paths:
            # Get all sub-paths in the directory
            for path in repo_path.rglob("*"):
                # Filter for only files (not dirs), and add to list.
                # Also, only add paths which aren't marked as excluded in the config.
                if path.is_file() and not self._is_excluded(path):
                    file_paths.add(str(path.resolve()))

        # Return filepaths as a list
        return sorted(file_paths)

    def main(self) -> List[str]:
        """Execute the app."""
        return self.run()
