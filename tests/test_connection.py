from src.notion.client import NotionClient

def test_notion_connection():
    """Test the connection to Notion API."""
    try:
        client = NotionClient()
        pages = client.get_database_pages()
        print("Successfully connected to Notion!")
        print(f"Found {len(pages)} pages in the database")
        return True
    except Exception as e:
        print(f"Failed to connect to Notion: {str(e)}")
        return False

if __name__ == "__main__":
    test_notion_connection() 