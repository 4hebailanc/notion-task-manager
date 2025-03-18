import json
from datetime import datetime
from notion.client import NotionClient
from notion.task import NotionTask, TaskStatus, TaskPriority

def import_tasks_from_json(json_file_path: str):
    """Import tasks from a JSON file into Notion."""
    # Initialize Notion client
    client = NotionClient()
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get project UUID
    project_name = data['tasks'][0]['pathin_projects'][0]  # Get project name from first task
    project_id = client.get_project_id_by_name(project_name)
    if not project_id:
        print(f"Error: Project '{project_name}' not found")
        return
    
    # Create tasks
    for task_data in data['tasks']:
        # Convert date string to datetime
        due_date = datetime.strptime(task_data['due'], '%Y-%m-%d')
        
        # Create NotionTask instance with project UUID
        task = NotionTask(
            title=task_data['title'],
            status=TaskStatus(task_data['status']),
            priority=TaskPriority(task_data['priority']),
            due=due_date,
            tags=task_data['tags'],
            pathin_projects=[project_id]  # Use project UUID instead of name
        )
        
        # Create task in Notion
        try:
            client.create_task(task)
            print(f"Successfully created task: {task.title}")
        except Exception as e:
            print(f"Failed to create task {task.title}: {str(e)}")

def main():
    """Main function to import webpage tasks."""
    json_file_path = "examples/webpage_tasks.json"
    import_tasks_from_json(json_file_path)

if __name__ == "__main__":
    main() 