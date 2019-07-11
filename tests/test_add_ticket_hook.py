from add_ticket_hook import __version__, add_ticket


def test_version():
    assert __version__ == "0.1.0"


def test_parse_tag():
    assert add_ticket.parse_tag("test-1235: anothu") == "test"
