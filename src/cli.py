import argparse
from datetime import datetime, timedelta
from typing import List
import json
import csv
from pathlib import Path

from notion.client import NotionClient
from notion.task import NotionTask, TaskStatus, TaskPriority

def create_tasks_from_csv(client: NotionClient, csv_path: str) -> List[dict]:
    """Create tasks from a CSV file.
    
    CSV format should be:
    title,assignee,status,due,priority,tags
    """
    tasks = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = NotionTask(
                title=row['title'],
                assignee=row.get('assignee'),
                status=TaskStatus(row.get('status', 'Not Started')),
                due=datetime.fromisoformat(row['due']) if row.get('due') else None,
                priority=TaskPriority(row.get('priority')) if row.get('priority') else None,
                tags=row.get('tags', '').split(';') if row.get('tags') else None
            )
            tasks.append(task)
    return client.create_tasks_batch(tasks)

def create_tasks_from_json(client: NotionClient, json_path: str) -> List[dict]:
    """Create tasks from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = [NotionTask(**task_data) for task_data in data]
    return client.create_tasks_batch(tasks)

def main():
    parser = argparse.ArgumentParser(description='Notion Task Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create tasks command
    create_parser = subparsers.add_parser('create', help='Create tasks')
    create_parser.add_argument('--csv', help='Create tasks from CSV file')
    create_parser.add_argument('--json', help='Create tasks from JSON file')
    create_parser.add_argument('--title', help='Task title')
    create_parser.add_argument('--assignee', help='Task assignee')
    create_parser.add_argument('--status', choices=[s.value for s in TaskStatus], default='Not Started')
    create_parser.add_argument('--priority', choices=[p.value for p in TaskPriority])
    create_parser.add_argument('--due', help='Due date (ISO format)')
    create_parser.add_argument('--tags', help='Semicolon-separated tags')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=[s.value for s in TaskStatus])
    list_parser.add_argument('--priority', choices=[p.value for p in TaskPriority])
    
    # Update task command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('page_id', help='Task page ID')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--assignee', help='New assignee')
    update_parser.add_argument('--status', choices=[s.value for s in TaskStatus])
    update_parser.add_argument('--priority', choices=[p.value for p in TaskPriority])
    update_parser.add_argument('--due', help='New due date (ISO format)')
    update_parser.add_argument('--tags', help='Semicolon-separated tags')
    
    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('page_id', help='Task page ID')
    
    args = parser.parse_args()
    client = NotionClient()
    
    if args.command == 'create':
        if args.csv:
            results = create_tasks_from_csv(client, args.csv)
            print(f"Created {len(results)} tasks from CSV")
        elif args.json:
            results = create_tasks_from_json(client, args.json)
            print(f"Created {len(results)} tasks from JSON")
        else:
            task = NotionTask(
                title=args.title,
                assignee=args.assignee,
                status=TaskStatus(args.status),
                priority=TaskPriority(args.priority) if args.priority else None,
                due=datetime.fromisoformat(args.due) if args.due else None,
                tags=args.tags.split(';') if args.tags else None
            )
            result = client.create_task(task)
            print(f"Created task: {result['id']}")
    
    elif args.command == 'list':
        if args.status:
            tasks = client.get_tasks_by_status(TaskStatus(args.status))
        elif args.priority:
            tasks = client.get_tasks_by_priority(TaskPriority(args.priority))
        else:
            tasks = [NotionTask.from_notion_page(page) for page in client.get_database_pages()]
        
        for task in tasks:
            print(f"Title: {task.title}")
            print(f"Assignee: {task.assignee or 'None'}")
            print(f"Status: {task.status.value}")
            print(f"Priority: {task.priority.value if task.priority else 'None'}")
            print(f"Due: {task.due}")
            print(f"Tags: {', '.join(task.tags) if task.tags else 'None'}")
            print("---")
    
    elif args.command == 'update':
        task = client.get_task(args.page_id)
        if args.title:
            task.title = args.title
        if args.assignee:
            task.assignee = args.assignee
        if args.status:
            task.status = TaskStatus(args.status)
        if args.priority:
            task.priority = TaskPriority(args.priority)
        if args.due:
            task.due = datetime.fromisoformat(args.due)
        if args.tags:
            task.tags = args.tags.split(';')
        
        result = client.update_task(args.page_id, task)
        print(f"Updated task: {result['id']}")
    
    elif args.command == 'delete':
        client.delete_task(args.page_id)
        print(f"Deleted task: {args.page_id}")

if __name__ == '__main__':
    main() 