import pytest
import add_ticket


@pytest.fixture
def options():
    return add_ticket.Options(possible_tags=("test",), strict=False)


def test_parse_tag():
    assert add_ticket.parse_tag("test-1235: anothu") == "test"


def test_is_tagged(options):
    assert add_ticket.is_tagged("test-1235: anothu", options) is True
