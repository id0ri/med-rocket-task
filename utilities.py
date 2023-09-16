import os.path

import requests
from datetime import datetime, date
from string import Template
from configure import *


def get_api(api):
    try:
        response = requests.get(api)
    except Exception as error:
        print('Не удалось получить API: ', error)
        return None
    else:
        return response.json()


def generate_task(user, tasks):
    tasks_completed_list, tasks_actually_list = [], []
    for task in tasks:
        if len(task["title"]) > TASK_LENGTH:
            title = '- ' + task["title"][:TASK_LENGTH] + '...'
        else:
            title = '- ' + task["title"]

        if task["completed"]:
            tasks_completed_list.append(title)
        else:
            tasks_actually_list.append(title)

    current_time = str(datetime.today().time())

    user_report = Template(PATTERN).substitute(
        company=user["company"]["name"],
        name=user["name"],
        email=user["email"],
        date=date.today().strftime('%d.%m.%Y'),
        time=current_time[:current_time.rfind(':')],
        tasks_all_count=len(tasks),
        tasks_actually_count=len(tasks_actually_list),
        tasks_actually='\n'.join(tasks_actually_list),
        tasks_completed_count=len(tasks_completed_list),
        tasks_completed='\n'.join(tasks_completed_list)
    )

    save_report(user_report, os.path.join(TASK_FOLDER_PATH, TRANSFER_FOLDER_PATH), user["name"])


def rename_report(path, name):
    try:
        with open(os.path.join(path, name), 'r') as old_report_file:
            time_info = old_report_file.readlines()[1].split()
    except Exception as error:
        print('Не удалось открыть файл: ', error)
    else:
        time = time_info[-1]
        date = '_'.join(time_info[-2].split('.'))
        try:
            os.rename(os.path.join(path, name), os.path.join(path, 'old_' + name + '-' + date + 'T' + time))
        except Exception as error:
            print('Не удалось переименовать файл: ', error)


def save_report(user_report, path, name):
    try:
        with open(os.path.join(path, name), 'w+') as report_file:
            report_file.write(user_report)
    except Exception as error:
        print('Ошибка сохранения отчета: ', error)


def update_reports(current_path, finally_path):
    for name in os.listdir(current_path):
        if os.path.exists(os.path.join(finally_path, name)):
            rename_report(finally_path, name)
        try:
            os.rename(os.path.join(current_path, name), os.path.join(finally_path, name))
        except Exception as error:
            print('Не удалось переместить файл: ', error)
    os.rmdir(current_path)


def check_for_failures():
    if os.path.isdir(TASK_FOLDER_PATH):
        if os.path.isdir(TASK_FOLDER_PATH + '/' + TRANSFER_FOLDER_PATH):
            dir_list = os.listdir(TASK_FOLDER_PATH + '/' + TRANSFER_FOLDER_PATH)
            if not dir_list:
                os.rmdir(TASK_FOLDER_PATH + '/' + TRANSFER_FOLDER_PATH)
            else:
                update_reports(TASK_FOLDER_PATH + '/' + TRANSFER_FOLDER_PATH, TASK_FOLDER_PATH)