from notion.client import NotionClient

def main():
    """Check the structure of the projects database."""
    client = NotionClient()
    
    try:
        # Get the projects database
        database = client.client.databases.retrieve(database_id=client.projects_database_id)
        
        print("\nProjects Database Properties:")
        for name, prop in database['properties'].items():
            print(f"\nProperty: {name}")
            print(f"Type: {prop['type']}")
            if prop['type'] == 'select':
                print("Options:", [opt['name'] for opt in prop.get('select', {}).get('options', [])])
            elif prop['type'] == 'multi_select':
                print("Options:", [opt['name'] for opt in prop.get('multi_select', {}).get('options', [])])
            elif prop['type'] == 'status':
                print("Options:", [opt['name'] for opt in prop.get('status', {}).get('options', [])])
            elif prop['type'] == 'title':
                print("This is the title property")
    except Exception as e:
        print(f"Error inspecting projects database: {str(e)}")

if __name__ == "__main__":
    main() 