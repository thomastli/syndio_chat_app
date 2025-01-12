import logging

import pytest
from unittest.mock import MagicMock
from ai.gpt_4o_mini import GPT4oMini

@pytest.fixture
def ai():
    """Fixture to create a GPT4oMini instance for each test."""
    return GPT4oMini()

@pytest.fixture
def mock_openai(mocker):
    """Fixture to mock OpenAI client and its responses."""
    mock_client = MagicMock()
    mocker.patch('ai.gpt_4o_mini.OpenAI', return_value=mock_client)
    return mock_client

def test_get_ai_response_success(ai, mock_openai):
    """Test successful API call and response."""
    expected_response = "This is a test response"
    
    # Mock the response structure
    mock_message = MagicMock()
    mock_message.content = expected_response
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    # Set up the mock chain
    mock_openai.chat.completions.create.return_value = mock_completion

    # Make the call
    response = ai.get_ai_response("Test message")

    # Verify response
    assert response == expected_response
    
    # Verify API was called with correct parameters
    mock_openai.chat.completions.create.assert_called_once_with(
        messages=[
            {
                "role": "user",
                "content": "Test message"
            }
        ],
        model="gpt-4o-mini",
    )

def test_get_ai_response_api_error(ai, mock_openai):
    """Test handling of API errors."""
    # Make the API call raise an exception
    mock_openai.chat.completions.create.side_effect = Exception("API Error")

    # Make the call
    response = ai.get_ai_response("Test message")

    # Verify error response
    assert response == "I apologize, but I'm having trouble processing your request."

def test_get_ai_response_empty_input(ai, mock_openai):
    """Test handling of empty input."""
    expected_response = "Empty input response"
    
    # Mock the response
    mock_message = MagicMock()
    mock_message.content = expected_response
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    mock_openai.chat.completions.create.return_value = mock_completion

    response = ai.get_ai_response("")
    
    assert response == expected_response
    mock_openai.chat.completions.create.assert_called_once()

def test_get_ai_response_missing_api_key(ai, mocker):
    """Test behavior when API key is missing."""
    # Mock os.environ.get to return None for API key
    mocker.patch('os.environ.get', return_value=None)
    
    response = ai.get_ai_response("Test message")
    assert response == "I apologize, but I'm having trouble processing your request."

def test_get_ai_response_logs_error(ai, mock_openai, caplog):
    """Test that errors are properly logged."""
    error_message = "API Error"
    mock_openai.chat.completions.create.side_effect = Exception(error_message)

    with caplog.at_level(logging.ERROR):
        ai.get_ai_response("Test message")
    
    assert f"Error calling LLM API: {error_message}" in caplog.text

@pytest.mark.parametrize("test_input", [
    "Hello",
    "   ",
    "123",
    "!@#$",
    "A" * 1000,  # Test with long input
])
def test_get_ai_response_handles_various_inputs(ai, mock_openai, test_input):
    """Test that various types of input are handled properly."""
    expected_response = "Test response"
    
    # Mock the response
    mock_message = MagicMock()
    mock_message.content = expected_response
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    mock_openai.chat.completions.create.return_value = mock_completion

    response = ai.get_ai_response(test_input)
    assert response == expected_response
    mock_openai.chat.completions.create.assert_called_once()
