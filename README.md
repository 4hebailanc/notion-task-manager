# Notion Task Manager

一个用于管理 Notion 任务的命令行工具，支持任务的创建、更新、删除和查询等功能。

## 功能特点

- 创建单个任务或批量导入任务
- 更新任务状态、优先级、截止日期等属性
- 删除任务
- 按状态、优先级等条件查询任务
- 支持从 CSV 和 JSON 文件批量导入任务
- 支持任务与项目的关联

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/notion-task-manager.git
cd notion-task-manager
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 Notion API：
   - 在 Notion 开发者页面获取 API Key
   - 复制 `config/credentials.yaml.example` 为 `config/credentials.yaml`
   - 在 `credentials.yaml` 中填入你的 API Key 和数据库 ID

## 使用方法

### 创建任务

```bash
# 创建单个任务
python src/cli.py create --title "任务标题" --status "Not Started" --priority "High" --due "2024-03-20" --tags "Development;UI/UX"

# 从 CSV 文件批量创建任务
python src/cli.py create --csv examples/tasks.csv

# 从 JSON 文件批量创建任务
python src/cli.py create --json examples/tasks.json
```

### 列出任务

```bash
# 列出所有任务
python src/cli.py list

# 按状态筛选任务
python src/cli.py list --status "In Progress"

# 按优先级筛选任务
python src/cli.py list --priority "High"
```

### 更新任务

```bash
python src/cli.py update <task_id> --status "Done" --priority "Medium"
```

### 删除任务

```bash
python src/cli.py delete <task_id>
```

## 项目结构

```
notion-task-manager/
├── config/
│   └── credentials.yaml
├── src/
│   ├── notion/
│   │   ├── client.py
│   │   └── task.py
│   ├── cli.py
│   └── import_webpage_tasks.py
├── examples/
│   └── webpage_tasks.json
├── tests/
│   └── test_task_creation.py
├── requirements.txt
└── README.md
```

## 开发

### 运行测试

```bash
pytest tests/
```

### 代码风格

项目使用 black 进行代码格式化：

```bash
black src/ tests/
```

## 许可证

MIT License 