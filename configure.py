TASKS_LIST_API = 'https://json.medrocket.ru/todos'
USERS_LIST_API = 'https://json.medrocket.ru/users'
TRANSFER_FOLDER_PATH = 'transfer'
TASK_FOLDER_PATH = 'tasks'
TASK_LENGTH = 46

PATTERN = '''# Отчет для ${company}.
$name <${email}> $date $time
Всего задач: $tasks_all_count

## Актуальные задачи(${tasks_actually_count}):
$tasks_actually

## Завершенные задачи(${tasks_completed_count}):
$tasks_completed
'''


