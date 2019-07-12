import subprocess


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


def get_current_branch_name():
    # type: () -> str
    try:
        branch_name = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        )
        return branch_name.strip(b" \n\t\r'\"").decode("utf-8")
    except (RuntimeError, AttributeError):
        return ""
