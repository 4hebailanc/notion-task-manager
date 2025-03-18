import pytest
from pathlib import Path
from src.notion.client import NotionClient

def test_notion_client_initialization():
    """Test that the NotionClient can be initialized."""
    # This is a basic test - in a real implementation, you would want to mock the API calls
    client = NotionClient()
    assert client is not None
    assert client.database_id is not None

def test_get_page_content():
    """Test retrieving page content."""
    client = NotionClient()
    # In a real test, you would mock the API response
    # For now, we'll just test that the method exists
    assert hasattr(client, 'get_page_content')

def test_get_database_pages():
    """Test retrieving database pages."""
    client = NotionClient()
    # In a real test, you would mock the API response
    # For now, we'll just test that the method exists
    assert hasattr(client, 'get_database_pages') 