import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv  # Ensure environment variables are loaded

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load .env file for local testing
load_dotenv()

# Mock replit.db and DISCORD_BOT_TOKEN before importing main.py
with patch("replit.db", new_callable=MagicMock) as mock_db, patch.dict(os.environ, {"DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN", "fake-token")}):
    mock_db.keys.return_value = ["responding"]
    mock_db.__contains__.side_effect = lambda key: key in ["responding"]
    mock_db.__getitem__.side_effect = lambda key: {"encouragements": ["Keep going!"]}[key] if key == "encouragements" else None
    mock_db.__setitem__.side_effect = lambda key, value: None  # Mock db set operation

    from main import is_abusive  # Import after mocking db

@pytest.mark.parametrize("message, expected", [
    ("This is a normal message", False),
    ("You are a bitch", True),
    ("Go to hell, mother fucker", True),
    ("Have a nice day!", False)
])
def test_is_abusive(message, expected):
    """Test if abusive words are correctly detected."""
    result = is_abusive(message)
    assert result == expected
