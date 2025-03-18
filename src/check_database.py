from notion.client import NotionClient

def main():
    client = NotionClient()
    database = client.inspect_database()
    
    if database:
        print("\nDatabase ID:", database['id'])
        print("Database Title:", database['title'][0]['text']['content'])

if __name__ == "__main__":
    main() 