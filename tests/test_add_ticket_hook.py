import pytest
from add_ticket_hook import main


@pytest.fixture
def options():
    return main.Options(prefixes=("test-", "lol-", "#"), strict=False)


@pytest.mark.parametrize(
    "message", ["test-124: anothu", "test-124", "test-124ASHT", "test-124-ASHT"]
)
def test_parse_ticket(message, options):
    assert main.parse_ticket(message, options) == "test-124"


@pytest.mark.parametrize("message", ["#123", "#123ASNTH", "#123."])
def test_parse_ticket_github_format(message, options):
    assert main.parse_ticket(message, options) == "#123"


def test_parse_another_ticket(options):
    assert main.parse_ticket("lol-123ARCGH", options) == "lol-123"


@pytest.mark.parametrize(
    "message",
    [
        "",
        "TEST-1234:aoseth",
        "t-1234:aoseth",
        "1234",
        "sthaoe test-1234 ",
        "test-",
        "test",
        "lol",
        "#",
        "#AENSH",
    ],
)
def test_ticket_not_found(message, options):
    assert main.parse_ticket(message, options) is None


@pytest.mark.parametrize(
    "args,filename,prefixes,strict",
    [
        (
            ["commitfile", "--prefixes='test-,lol-'"],
            "commitfile",
            ["test-", "lol-"],
            False,
        ),
        (["commitfile", "--prefixes='test-'", "-s"], "commitfile", ["test-"], True),
        (
            ["commitfile", "--prefixes='test-'", "--strict"],
            "commitfile",
            ["test-"],
            True,
        ),
        (["commitfile", "-p 'test-'"], "commitfile", ["test-"], False),
        (["commitfile", "-p '#'"], "commitfile", ["#"], False),
        (["commitfile", "-p test-"], "commitfile", ["test-"], False),
        (["commitfile", "-p test-", "-p lol-"], "commitfile", ["test-", "lol-"], False),
        (
            ["commitfile", "-p test-", "-p ',lol-'"],
            "commitfile",
            ["test-", "lol-"],
            False,
        ),
        (
            ["commitfile", "--prefixes='test-'", "--strict", "-p lol-"],
            "commitfile",
            ["test-", "lol-"],
            True,
        ),
    ],
)
def test_parse_args(args, filename, prefixes, strict):
    _filename, options = main.parse_args(args)
    assert _filename == filename
    assert options.prefixes == prefixes
    assert options.strict is strict


@pytest.mark.parametrize(
    "message,branch_name,alt_msg",
    [
        ("", "", ""),
        ("", "test-13", "test-13: "),
        ("", "__", ""),
        ("", "test", ""),
        ("test-1234", "", "test-1234"),
        ("random... test-1234", "", "random... test-1234"),
        ("random... test-1234", "lol-1", "lol-1: random... test-1234"),
        ("random... test-1234", "lol-1ARC", "lol-1: random... test-1234"),
    ],
)
def test_alter_message(message, branch_name, alt_msg, options):
    assert main.alter_message(message, branch_name, options) == alt_msg


@pytest.mark.parametrize(
    "message,branch_name,alt_msg",
    [
        ("", "", ""),
        ("", "__", ""),
        ("", "test", ": "),
        ("random... test-1234", "", "random... test-1234"),
    ],
)
def test_alter_message_strict(message, branch_name, alt_msg):
    options = main.Options(prefixes=("test-", "lol-"), strict=True)
    with pytest.raises(ValueError):
        main.alter_message(message, branch_name, options)
