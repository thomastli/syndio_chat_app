from unittest.mock import patch

import pytest

from ai.dummy_ai import DummyAI, DUMMY_RESPONSES


@pytest.fixture
def ai():
    """Fixture to create a DummyAI instance for each test."""
    return DummyAI()


def test_get_ai_response_returns_string(ai):
    """Test that get_ai_response returns a string."""
    response = ai.get_ai_response("Hello")
    assert isinstance(response, str)


def test_get_ai_response_returns_valid_response(ai):
    """Test that get_ai_response returns a response from the valid set."""
    response = ai.get_ai_response("Test message")
    assert response in DUMMY_RESPONSES


def test_get_ai_response_uses_random_choice(ai):
    """Test that get_ai_response uses random.choice to select response.
    The mocker fixture is provided by pytest-mock."""
    with patch('ai.dummy_ai.random.choice') as mock:
        mock.return_value = DUMMY_RESPONSES[0]
        response = ai.get_ai_response("Test message")
        assert response == DUMMY_RESPONSES[0]


def test_get_ai_response_handles_empty_input(ai):
    """Test that get_ai_response handles empty string input."""
    response = ai.get_ai_response("")
    assert response in DUMMY_RESPONSES


@pytest.mark.parametrize("test_input,expected_type", [
    ("Hello", str),
    ("", str),
    ("   ", str),
    ("123", str),
    ("!@#$", str),
])
def test_get_ai_response_returns_string_for_various_inputs(ai, test_input, expected_type):
    """Test that get_ai_response returns string for various input types."""
    response = ai.get_ai_response(test_input)
    assert isinstance(response, expected_type)


def test_get_ai_response_random_distribution(ai):
    """Test that get_ai_response provides responses with roughly even distribution."""
    responses = [ai.get_ai_response("test") for _ in range(1000)]

    # Check that each response appears at least once
    unique_responses = set(responses)
    assert unique_responses.issubset(set(DUMMY_RESPONSES))

    # Check that each response appears roughly the expected number of times
    # (with some margin for randomness)
    expected_count = 1000 / len(DUMMY_RESPONSES)
    for response in DUMMY_RESPONSES:
        count = responses.count(response)
        # Allow for 30% deviation from expected count
        assert expected_count * 0.7 <= count <= expected_count * 1.3