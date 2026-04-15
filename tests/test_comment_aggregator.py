from pathlib import Path

from commentAggregator import commentAggregator
from fileParser import ParsedComment


def build_comment(file_path: Path, line_number: int, keyword: str) -> ParsedComment:
    """Build a fake comment object for testing"""

    return ParsedComment(
        file_path=str(file_path.resolve()),
        line_number=line_number,
        keyword=keyword,
        line_content=f"{keyword} marker",
    )


def test_aggregate_by_file_groups_comments_and_sorts_by_line_number(tmp_path):
    """Test that aggregate_by_file correctly groups comments"""

    # Set up temporary files
    file_a = tmp_path / "area" / "a.py"
    file_b = tmp_path / "area" / "b.py"

    # Add comment objects into a list, in order to aggregate later
    comments = [
        build_comment(file_a, 2, "NOTE"),
        build_comment(file_a, 8, "TODO"),
        build_comment(file_b, 3, "BUG"),
    ]

    # Aggregate comments per file
    grouped = commentAggregator(comments).aggregate_by_file()

    # Capture the two file groups
    # first_group should correspond to file a
    first_group = grouped[0]
    # second_group should correspond to file b
    second_group = grouped[1]

    # Assert that the paths are correct
    assert first_group.file_path == str(file_a.resolve())
    assert second_group.file_path == str(file_b.resolve())

    # Assert that the line numbers are correct
    assert grouped[0].comments[0].line_number == 2
    assert grouped[0].comments[1].line_number == 8
    assert grouped[1].comments[0].line_number == 3

    # Assert that the counts are correct
    assert grouped[0].keyword_counts() == {"NOTE": 1, "TODO": 1}
    assert grouped[1].keyword_counts() == {"BUG": 1}


def test_all_keyword_counts_combines_counts_across_all_files(tmp_path):
    """Test that all_keyword_counts adds up keyword occurances correctly"""

    # Set up temp files
    file_a = tmp_path / "a.py"
    file_b = tmp_path / "b.py"

    # Add comment objects into a list, in order to aggregate later
    comments = [
        build_comment(file_a, 1, "TODO"),
        build_comment(file_a, 5, "TODO"),
        build_comment(file_b, 3, "BUG"),
    ]

    # Test that keywords are being correctly counted.
    counts = commentAggregator(comments).all_keyword_counts()
    assert counts == {"TODO": 2, "BUG": 1}
