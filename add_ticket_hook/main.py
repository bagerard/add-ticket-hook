""" commit-msg hook for git.

Hook checks and alters commit message content based
on given rules.

Commits themselves should use convention::

    'TAG-1234: Commit message'

To us branch as basis for commit message creation. Then they should start with::

    TAG-1234

This means that following branch names are okay::

    TAG-1234
    TAG-1234_human_readable
    TAG-1234.human.readable
    TAG-1234HUMANREADABLE

as long next char after ticket number is not digit, its okay.
"""
from __future__ import print_function

import sys
import re
import typing  # noqa
import argparse

from collections import namedtuple
from . import io


Options = namedtuple("Options", "possible_tags,strict")


def parse_args(argv=None):
    # type: (typing.Optional[typing.Sequence[str]]) -> typing.Tuple[str, Options]
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Commit filename")
    parser.add_argument(
        "-t",
        "--tags",
        action="append",
        help="Possible tags that could be ticket prefixes. Comma separated list.",
    )
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Fail if no tag is found",
        default=False,
    )
    args = parser.parse_args(argv)

    assert args.filenames, "No commit filename given"
    assert args.tags, "No tags specified in config"

    tags = parse_tags(args.tags)

    return (args.filenames[0], Options(possible_tags=tags, strict=args.strict))


def parse_tags(tags):
    # type: (typing.List[str]) -> typing.List[str]
    tags_str = ",".join(tags)
    for char in "\"' ":
        tags_str = tags_str.replace(char, "")

    return [tag for tag in tags_str.split(",") if tag]


def is_tagged(message, options):
    # type: (str, Options) -> bool
    """ check if commit message has already a tag in it.
    """
    found_tag = message.split("-")[0].strip()
    return found_tag in options.possible_tags


def parse_tagnum_from_branch(branch_name):
    # type: (str) -> typing.List[str]
    match = re.match(r"^[a-zA-Z]*-\d*", branch_name)
    if match:
        stripped_name = match.group()
        return stripped_name.split("-")
    return ["", ""]


def get_tagnum_from_branch(branch_name, options):
    # type: (str, Options) -> str
    tag, ticket_number = parse_tagnum_from_branch(branch_name)

    if tag in options.possible_tags:
        return "{}-{}".format(tag, ticket_number)
    return ""


def alter_message(message, branch_name, options):
    # type: (str, str, Options) -> str
    """ Alter message content if needed

    tag is not added if it cannot be parsed from branch,
    or it already exists.

    Args:
        message: original commit message
        branch_name: name of current branch
        options: settings for this hook

    Returns:
        altered message that includes ticket prefix (probably)
    """
    commit_is_tagged = is_tagged(message, options)

    # commit is already tagged, nothing to do here
    if commit_is_tagged:
        return message

    branch_is_tagged = is_tagged(branch_name, options)

    if branch_is_tagged:
        tag = get_tagnum_from_branch(branch_name, options)
        return "{}: {}".format(tag, message)

    if options.strict:
        raise ValueError(
            "ERROR: We are using strict mode and no ticket was "
            "specified in commit message nor branch name."
        )

    return message


def main():
    # type: () -> int
    try:
        filename, options = parse_args(sys.argv[1:])
        branch_name = io.get_current_branch_name()
        message = io.read_commit_message(filename)
        altered_message = alter_message(message, branch_name, options)
        io.write_commit_message(filename, altered_message)
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    exit(main())
