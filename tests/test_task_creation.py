import pytest
from datetime import datetime, timedelta
from src.notion.task import NotionTask, TaskStatus, TaskPriority
from src.notion.client import NotionClient

def test_create_single_task():
    """Test creating a single task."""
    client = NotionClient()
    
    # Create a test task
    task = NotionTask(
        title="测试任务",
        status=TaskStatus.NOT_STARTED,
        priority=TaskPriority.MEDIUM,
        due_date=datetime.now() + timedelta(days=7),
        description="这是一个测试任务",
        tags=["测试", "重要"]
    )
    
    # Create the task in Notion
    result = client.create_task(task)
    assert result is not None
    assert result['id'] is not None
    
    # Clean up - delete the task
    client.delete_task(result['id'])

def test_create_multiple_tasks():
    """Test creating multiple tasks."""
    client = NotionClient()
    
    # Create test tasks
    tasks = [
        NotionTask(
            title=f"测试任务 {i}",
            status=TaskStatus.NOT_STARTED,
            priority=TaskPriority.MEDIUM,
            due_date=datetime.now() + timedelta(days=i),
            description=f"这是测试任务 {i}",
            tags=["测试", f"任务{i}"]
        )
        for i in range(3)
    ]
    
    # Create the tasks in Notion
    results = client.create_tasks_batch(tasks)
    assert len(results) == 3
    
    # Clean up - delete the tasks
    for result in results:
        client.delete_task(result['id'])

def test_task_properties():
    """Test task properties conversion."""
    task = NotionTask(
        title="测试任务",
        status=TaskStatus.NOT_STARTED,
        priority=TaskPriority.HIGH,
        due_date=datetime.now(),
        description="测试描述",
        tags=["测试", "标签"]
    )
    
    properties = task.to_notion_properties()
    assert properties["Name"]["title"][0]["text"]["content"] == "测试任务"
    assert properties["Status"]["select"]["name"] == "Not Started"
    assert properties["Priority"]["select"]["name"] == "High"
    assert "Due Date" in properties
    assert properties["Description"]["rich_text"][0]["text"]["content"] == "测试描述"
    assert len(properties["Tags"]["multi_select"]) == 2 