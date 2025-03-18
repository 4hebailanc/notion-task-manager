from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    ARCHIVED = "Archived"

class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

@dataclass
class NotionTask:
    title: str
    assignee: Optional[List[str]] = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    due: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    parent_task: Optional[List[str]] = None
    sub_tasks: Optional[List[str]] = None
    pathin_projects: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    blocked_by: Optional[List[str]] = None
    is_blocking: Optional[List[str]] = None

    def to_notion_properties(self) -> Dict:
        """Convert task to Notion properties format."""
        properties = {
            "Task name": {"title": [{"text": {"content": self.title}}]},
            "Status": {"status": {"name": self.status.value}},
            "Assignee": {"people": self.assignee if self.assignee else []},
        }
        
        if self.due:
            properties["Due"] = {"date": {"start": self.due.isoformat()}}
        
        if self.priority:
            properties["Priority"] = {"select": {"name": self.priority.value}}
        
        if self.parent_task:
            properties["Parent-task"] = {"relation": [{"id": id} for id in self.parent_task]}
        
        if self.sub_tasks:
            properties["Sub-tasks"] = {"relation": [{"id": id} for id in self.sub_tasks]}
        
        if self.pathin_projects:
            properties["Pathin Projects"] = {"relation": [{"id": id} for id in self.pathin_projects]}
        
        if self.tags:
            properties["Tags"] = {"multi_select": [{"name": tag} for tag in self.tags]}
        
        if self.blocked_by:
            properties["Blocked By"] = {"relation": [{"id": id} for id in self.blocked_by]}
        
        if self.is_blocking:
            properties["Is Blocking"] = {"relation": [{"id": id} for id in self.is_blocking]}
        
        return properties

    @classmethod
    def from_notion_page(cls, page: Dict) -> 'NotionTask':
        """Create a NotionTask from a Notion page."""
        properties = page['properties']
        
        # Extract title
        title = properties.get('Task name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        
        # Extract assignee (people type)
        assignee = [user['id'] for user in properties.get('Assignee', {}).get('people', [])]
        
        # Extract status
        status_value = properties.get('Status', {}).get('status', {}).get('name', 'Not Started')
        status = TaskStatus(status_value)
        
        # Extract due date
        due_date_str = properties.get('Due', {}).get('date', {}).get('start')
        due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        
        # Extract priority
        priority_value = properties.get('Priority', {}).get('select', {}).get('name')
        priority = TaskPriority(priority_value) if priority_value else None
        
        # Extract parent task
        parent_task = [rel['id'] for rel in properties.get('Parent-task', {}).get('relation', [])]
        
        # Extract sub tasks
        sub_tasks = [rel['id'] for rel in properties.get('Sub-tasks', {}).get('relation', [])]
        
        # Extract Pathin Projects
        pathin_projects = [rel['id'] for rel in properties.get('Pathin Projects', {}).get('relation', [])]
        
        # Extract tags
        tags = [tag['name'] for tag in properties.get('Tags', {}).get('multi_select', [])]
        
        # Extract blocked by
        blocked_by = [rel['id'] for rel in properties.get('Blocked By', {}).get('relation', [])]
        
        # Extract is blocking
        is_blocking = [rel['id'] for rel in properties.get('Is Blocking', {}).get('relation', [])]
        
        return cls(
            title=title,
            assignee=assignee if assignee else None,
            status=status,
            due=due_date,
            priority=priority,
            parent_task=parent_task if parent_task else None,
            sub_tasks=sub_tasks if sub_tasks else None,
            pathin_projects=pathin_projects if pathin_projects else None,
            tags=tags if tags else None,
            blocked_by=blocked_by if blocked_by else None,
            is_blocking=is_blocking if is_blocking else None
        ) 