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

import re
import typing
import argparse

from collections import namedtuple
from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


Options = namedtuple("Options", "possible_tags,strict")


def read_commit_message(filename):
    # type: (str) -> str
    """ Read original commit message from file
    """
    with open(filename, "r+") as f:
        return f.read().strip()


def write_commit_message(filename, message):
    # type: (str, str) -> None
    """ Write new commit message to file
    """
    with open(filename, "r+") as f:
        f.seek(0)
        f.write(message)
        f.truncate()


def parse_tag(message):
    # type: (str) -> str
    """ parse possible tag from message
    """
    return message.split("-")[0].strip()


def parse_tagnum_from_branch(branch_name):
    # type: (str) -> typing.List[str]
    match = re.match(r"^[A-Z]*-\d*", branch_name)
    if match:
        stripped_name = match.group()
        return stripped_name.split("-")
    return ["", ""]


def is_tagged(message, options):
    # type: (str, Options) -> bool
    """ check if commit message has already a tag in it.
    """
    tags = options.possible_tags
    possible_tag = parse_tag(message)
    return possible_tag in tags


def get_tagnum_from_branch(branch_name, options):
    # type: (str, Options) -> str
    tags = options.possible_tags
    tag, ticket_number = parse_tagnum_from_branch(branch_name)

    if tag in tags:
        return "{}-{}".format(tag, ticket_number)
    return ""


def write_tagnum(filename, message, tag=None):
    # type: (str, str, typing.Optional[str]) -> None
    """ write tagnum to commit message.

    add tag if exists
    """
    if tag is not None:
        write_commit_message(filename, "{}: {}".format(tag, message))


def alter_message(filename, branch_name, options):
    # type: (str, str, Options) -> None
    """ Alter message content if needed

    tag is not added if it cannot be parsed from branch,
    or it already exists.

    Args:
        filename: filename of commit file
        branch_name: name of current branch
        options: settings for this hook
    """
    message = read_commit_message(filename)
    branch_is_tagged = is_tagged(branch_name, options)
    commit_is_tagged = is_tagged(message, options)
    if not commit_is_tagged and branch_is_tagged:
        write_tagnum(filename, message, get_tagnum_from_branch(branch_name, options))
    elif not commit_is_tagged and not branch_is_tagged and options.strict:
        raise ValueError(
            "ERROR: We are using strict mode and no ticket was "
            "specified in commit message nor branch name."
        )


def get_current_branch_name():
    # type: () -> str
    try:
        branch_name = cmd_output("git", "rev-parse", "--abbrev-ref", "HEAD")
        return branch_name.strip()
    except (CalledProcessError, AttributeError):
        return ""


def parse_args(argv):
    # type: (typing.Optional[typing.Sequence[str]]) -> typing.Tuple[str, Options]
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Commit filename")
    parser.add_argument(
        "-t",
        "--tags",
        action="append",
        help="Possible tags that could be ticket prefixes.",
    )
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Fail if no tag is found",
        default=False,
    )
    args = parser.parse_args(argv)
    return (args.filenames[0], Options(possible_tags=args.tags, strict=args.strict))


def main(argv=None):
    # type: (typing.Optional[typing.Sequence[str]]) -> int
    try:
        filename, options = parse_args(argv)
        branch_name = get_current_branch_name()

        alter_message(filename=filename, branch_name=branch_name, options=options)
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    exit(main())
