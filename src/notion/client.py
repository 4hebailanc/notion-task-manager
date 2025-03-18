from typing import Dict, List, Optional
from notion_client import Client
import yaml
import os
from pathlib import Path
from datetime import datetime
from .task import NotionTask, TaskStatus, TaskPriority

class NotionClient:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Notion client with configuration.
        
        Args:
            config_path: Path to the credentials.yaml file. If None, will look for it in config/credentials.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "credentials.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.client = Client(auth=config['notion']['api_key'])
        self.database_id = config['notion']['database_id']
        self.projects_database_id = config['notion'].get('projects_database_id')
    
    def get_project_id_by_name(self, project_name: str) -> Optional[str]:
        """Get project UUID by name.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Project UUID if found, None otherwise
        """
        if not self.projects_database_id:
            raise ValueError("Projects database ID not configured")
            
        response = self.client.databases.query(
            database_id=self.projects_database_id,
            filter={
                "property": "Project name",
                "title": {
                    "equals": project_name
                }
            }
        )
        
        if response['results']:
            return response['results'][0]['id']
        return None
    
    def get_page_content(self, page_id: str) -> Dict:
        """Retrieve content from a Notion page.
        
        Args:
            page_id: The ID of the Notion page
            
        Returns:
            Dict containing the page content
        """
        return self.client.pages.retrieve(page_id=page_id)
    
    def get_database_pages(self) -> List[Dict]:
        """Retrieve all pages from the configured database.
        
        Returns:
            List of page objects from the database
        """
        return self.client.databases.query(database_id=self.database_id)['results']
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Update a Notion page with new properties.
        
        Args:
            page_id: The ID of the page to update
            properties: Dictionary of properties to update
            
        Returns:
            Updated page object
        """
        return self.client.pages.update(page_id=page_id, properties=properties)
    
    def create_task(self, task: NotionTask) -> Dict:
        """Create a single task in Notion.
        
        Args:
            task: NotionTask object containing task details
            
        Returns:
            Created page object from Notion API
        """
        return self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=task.to_notion_properties()
        )
    
    def create_tasks_batch(self, tasks: List[NotionTask]) -> List[Dict]:
        """Create multiple tasks in Notion.
        
        Args:
            tasks: List of NotionTask objects
            
        Returns:
            List of created page objects
        """
        return [self.create_task(task) for task in tasks]
    
    def get_task(self, page_id: str) -> NotionTask:
        """Retrieve a task by its page ID.
        
        Args:
            page_id: The ID of the task page
            
        Returns:
            NotionTask object
        """
        page = self.get_page_content(page_id)
        return NotionTask.from_notion_page(page)
    
    def update_task(self, page_id: str, task: NotionTask) -> Dict:
        """Update an existing task.
        
        Args:
            page_id: The ID of the task to update
            task: Updated NotionTask object
            
        Returns:
            Updated page object
        """
        return self.update_page(page_id, task.to_notion_properties())
    
    def delete_task(self, page_id: str) -> None:
        """Delete a task by its page ID.
        
        Args:
            page_id: The ID of the task to delete
        """
        self.client.pages.update(page_id=page_id, archived=True)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[NotionTask]:
        """Get all tasks with a specific status.
        
        Args:
            status: TaskStatus to filter by
            
        Returns:
            List of NotionTask objects
        """
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Status",
                "select": {
                    "equals": status.value
                }
            }
        )
        return [NotionTask.from_notion_page(page) for page in response['results']]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[NotionTask]:
        """Get all tasks with a specific priority.
        
        Args:
            priority: TaskPriority to filter by
            
        Returns:
            List of NotionTask objects
        """
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Priority",
                "select": {
                    "equals": priority.value
                }
            }
        )
        return [NotionTask.from_notion_page(page) for page in response['results']]
    
    def inspect_database(self) -> Dict:
        """Inspect database structure and properties."""
        try:
            database = self.client.databases.retrieve(database_id=self.database_id)
            print("\nDatabase Properties:")
            for name, prop in database['properties'].items():
                print(f"\nProperty: {name}")
                print(f"Type: {prop['type']}")
                if prop['type'] == 'select':
                    print("Options:", [opt['name'] for opt in prop.get('select', {}).get('options', [])])
                elif prop['type'] == 'multi_select':
                    print("Options:", [opt['name'] for opt in prop.get('multi_select', {}).get('options', [])])
                elif prop['type'] == 'status':
                    print("Options:", [opt['name'] for opt in prop.get('status', {}).get('options', [])])
            return database
        except Exception as e:
            print(f"Error inspecting database: {str(e)}")
            return None 