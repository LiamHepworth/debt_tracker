from fileParser import ParsedComment, fileParser


def test_run_extracts_default_keywords(tmp_path):
    """Test that the fileparser extracts default keywords from a file case insensitively"""

    # Create temp file and write to it
    sample = tmp_path / "sample.py"
    sample.write_text(
        "# TODO: first task\n" "print('ignore me')\n" "# note: second task\n",
        encoding="utf-8",
    )

    # Run parser on the temp file
    parsed_comments = fileParser([sample]).run()

    # Assert that both comments are extracted properly
    assert parsed_comments == [
        ParsedComment(
            file_path=str(sample.resolve()),
            line_number=1,
            keyword="TODO",
            line_content="# TODO: first task",
        ),
        ParsedComment(
            file_path=str(sample.resolve()),
            line_number=3,
            keyword="NOTE",
            line_content="# note: second task",
        ),
    ]


def test_custom_keywords_override_defaults(tmp_path):
    """Test that custom keywords override the defaults"""

    # Create temp file and write to it
    sample = tmp_path / "sample.txt"
    sample.write_text(
        "# FIXME: custom marker\n"
        "# TODO: should not match when defaults are overridden\n",
        encoding="utf-8",
    )

    # Parse the file, overriding default keywords
    parsed_comments = fileParser([sample], keywords=["fixme"]).run()

    # Assert comment is extracted correctly
    assert parsed_comments == [
        ParsedComment(
            file_path=str(sample.resolve()),
            line_number=1,
            keyword="FIXME",
            line_content="# FIXME: custom marker",
        )
    ]
