import pytest
from add_ticket_hook import main


@pytest.fixture
def options():
    return main.Options(possible_tags=("test", "lol"), strict=False)


@pytest.mark.parametrize(
    "message",
    ["test-1235: anothu", "test-1", "test-12.", "test-124ASHT", "test-124-ASHT"],
)
def test_is_tagged(message, options):
    assert main.is_tagged(message, options) is True


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
    ],
)
def test_is_not_tagged(message, options):
    assert main.is_tagged(message, options) is False


@pytest.mark.parametrize(
    "message", ["test-124: anothu", "test-124", "test-124ASHT", "test-124-ASHT"]
)
def test_parse_ticket(message, options):
    assert main.get_ticket_from_branch(message, options) == "test-124"


def test_parse_another_tagnum(options):
    assert main.get_ticket_from_branch("lol-123ARCGH", options) == "lol-123"


@pytest.mark.parametrize(
    "message", ["", "TEST-1234:aoseth", "t-1234:aoseth", "1234", "sthaoe test-1234 "]
)
def test_tag_num_not_found(message, options):
    assert main.get_ticket_from_branch(message, options) == ""


@pytest.mark.parametrize(
    "args,filename,tags,strict",
    [
        (["commitfile", "--tags='test,lol'"], "commitfile", ["test", "lol"], False),
        (["commitfile", "--tags='test'", "-s"], "commitfile", ["test"], True),
        (["commitfile", "--tags='test'", "--strict"], "commitfile", ["test"], True),
        (["commitfile", "-t 'test'"], "commitfile", ["test"], False),
        (["commitfile", "-t test"], "commitfile", ["test"], False),
        (["commitfile", "-t test", "-t lol"], "commitfile", ["test", "lol"], False),
        (["commitfile", "-t test", "-t ',lol'"], "commitfile", ["test", "lol"], False),
        (
            ["commitfile", "--tags='test'", "--strict", "-t lol"],
            "commitfile",
            ["test", "lol"],
            True,
        ),
    ],
)
def test_parse_args(args, filename, tags, strict):
    _filename, options = main.parse_args(args)
    assert _filename == filename
    assert options.possible_tags == tags
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
    options = main.Options(possible_tags=("test", "lol"), strict=True)
    with pytest.raises(ValueError):
        main.alter_message(message, branch_name, options)
