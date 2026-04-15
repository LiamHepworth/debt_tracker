import json
import pytest
from fileScanner import fileScanner


def test_load_exclude_suffixes_normalizes_case_and_removes_duplicates(tmp_path):
    """Test that load_exclude_suffixes normalises the case of each extension, and removes duplicates"""

    # Create temp config and write to it
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"exclude_suffixes": [".PY", ".txt", ".py"]}),
        encoding="utf-8",
    )

    # Load the config
    suffixes = fileScanner.load_exclude_suffixes(config)

    # Assert that duplicates are removed, and that cases are converted.
    assert suffixes == {".py", ".txt"}


def test_run_returns_applies_excludes(tmp_path):
    """Test that the run function returns sorted absolute paths, and correctly applies excludes."""

    # Set up mock repo path
    repo = tmp_path / "repo"
    nested = repo / "nested"
    nested.mkdir(parents=True)

    # Set up mock files
    keep_a = repo / "keep.py"
    keep_b = nested / "keep.txt"
    skip_a = repo / "ignore.pyc"
    skip_b = nested / "ignore.log"

    # Write to mock files
    keep_a.write_text("print('a')\n", encoding="utf-8")
    keep_b.write_text("notes\n", encoding="utf-8")
    skip_a.write_text("compiled\n", encoding="utf-8")
    skip_b.write_text("ignored\n", encoding="utf-8")

    # Set up config to exclude .pyc and .log files
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"exclude_suffixes": [".pyc", ".log"]}),
        encoding="utf-8",
    )

    # Run the filescanner to extract all absolute paths
    discovered_files = fileScanner([repo], config_path=config).run()

    # Assert that paths are sorted, absolute, and exclude the files
    # referenced in config.exclude_suffixes
    assert discovered_files == sorted(
        [
            str(keep_a.resolve()),
            str(keep_b.resolve()),
        ]
    )
