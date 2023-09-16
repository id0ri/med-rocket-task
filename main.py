from utilities import *
import os


def main():
    check_for_failures()

    task_data = get_api(TASKS_LIST_API)
    user_data = get_api(USERS_LIST_API)

    if task_data and user_data:
        task_data[:] = [task for task in task_data if len(task) == 4]

        if not os.path.isdir(TASK_FOLDER_PATH):
            os.mkdir(TASK_FOLDER_PATH)

        os.mkdir(os.path.join(TASK_FOLDER_PATH, TRANSFER_FOLDER_PATH))

        for user in user_data:
            tasks = [task for task in task_data if task["userId"] == user["id"]]
            generate_task(user, tasks)

        update_reports(os.path.join(TASK_FOLDER_PATH, TRANSFER_FOLDER_PATH), TASK_FOLDER_PATH)


if __name__ == "__main__":
    main()