""" commit-msg hook for git.

Hook checks and alters commit message content based
on given rules.

Commits themselves should use convention::

    '<prefix>1234: Commit message'

To use branch as basis for commit message creation. Then they should start with::

    <prefix>1234

This means that following branch names are okay::

    <prefix>1234
    <prefix>1234_human_readable
    <prefix>1234.human.readable
    <prefix>1234HUMANREADABLE

as long next char after ticket number is not digit, its okay.
"""
from __future__ import print_function

import sys
import re
import typing  # noqa
import argparse

from collections import namedtuple
from . import io


Options = namedtuple("Options", "prefixes,strict")


def parse_args(argv=None):
    # type: (typing.Optional[typing.Sequence[str]]) -> typing.Tuple[str, Options]
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Commit filename")
    parser.add_argument(
        "-p",
        "--prefixes",
        action="append",
        help="Possible ticket prefixes. Comma separated list.",
    )
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Fail if no ticket is found",
        default=False,
    )
    args = parser.parse_args(argv)

    assert args.filenames, "No commit filename given"
    assert args.prefixes, "No prefixes specified in config"

    prefixes = parse_prefixes(args.prefixes)

    return (args.filenames[0], Options(prefixes=prefixes, strict=args.strict))


def parse_prefixes(prefixes):
    # type: (typing.List[str]) -> typing.List[str]
    prefix_str = ",".join(prefixes)
    for char in "\"' ":
        prefix_str = prefix_str.replace(char, "")

    return [prefix for prefix in prefix_str.split(",") if prefix]


def parse_ticket(text, options):
    # type: (str, Options) -> typing.Optional[str]
    pattern = r"^(?P<ticket>{})(\d+)".format("|".join(options.prefixes))
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    return None


def alter_message(message, branch_name, options):
    # type: (str, str, Options) -> str
    """ Alter message content if needed

    prefix is not added if it cannot be parsed from branch,
    or it already exists.

    Args:
        message: original commit message
        branch_name: name of current branch
        options: settings for this hook

    Returns:
        altered message that includes ticket prefix (probably)
    """
    ticket_from_commit = parse_ticket(message, options)

    if ticket_from_commit:
        return message

    ticket_from_branch = parse_ticket(branch_name, options)

    if ticket_from_branch:
        default_commit_message = message.startswith("# Please enter the commit message")
        if default_commit_message:
            return "{}:\n{}".format(ticket_from_branch, message)
        else:
            return "{}: {}".format(ticket_from_branch, message)

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
