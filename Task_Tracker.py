import json

tasks = []
class Task:
    def __init__(self, task : str, status = 1):
        self.task = task
        if status == 1:
            self.progress = 'to do'
        elif status == 2:
            self.progress = 'in progress'
        elif status == 3:
            self.progress = 'done'
        else:
            print("Invalid progress.")

def enter_task():
    task_to_add = input("Enter the task: ")
    task_to_add = task_to_add[0].upper() + task_to_add[1:]
    progress = int(input("Enter the progress(1 - to do, 2 - in progress, 3 - done): "))
    return Task(task_to_add, progress).__dict__
def task_printable(place_of_the_task, task : dict = None, *, reason ='normal'):
    if not task:
        task = tasks[place_of_the_task-1]
    if reason == 'normal':
        return f"Task №{place_of_the_task}: {task['task']} - {task['progress']}"
    elif reason == 'delete':
        return f"Task №{place_of_the_task}: {task['task']}' was successfully deleted."
    elif reason == 'progress':
        return f"The progress of Task №{place_of_the_task} '{task['task']}' became {task['progress']}."
    else:
        return f"Type a proper reason."
def get_tasks():
    global tasks
    try:
        with open('Task_Storage.json', 'r') as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
def set_tasks():
    global tasks
    with open('Task_Storage.json', 'w') as f:
        json.dump(tasks, f, indent=4)
def add_task():
    global tasks
    get_tasks()
    new_task = enter_task()
    tasks.append(new_task)
    set_tasks()
    print(f"Task added.")
def delete_task(place_of_the_task : int):
    global tasks
    get_tasks()
    try:
        print(task_printable(place_of_the_task, reason ="delete"))
        tasks.remove(tasks[place_of_the_task-1])
    except IndexError:
        print("Index out of range")
    set_tasks()
def clear_tasks():
    global tasks
    input_ = input("Are you sure?(y/n): ").lower()
    if input_ == 'y':
        tasks = []
        set_tasks()
        print("All tasks cleared.")
def list_tasks(which = 'all'):
    global tasks
    get_tasks()
    if tasks:
        if which == 'all':
            print("Tasks".center(30, "-"))
            for i, task_ in enumerate(tasks, 1):
                print(task_printable(i, task_))
            print('-'*30)
        elif which == 'to do' or which == 'in progress' or which == 'done':
            for i, task_ in enumerate(tasks, 1):
                if task_['progress'] == which:
                    print(task_printable(i, task_))
        else:
            print("Invalid choice.")
    else:
        print("No tasks")
def update_task(place_of_the_task : int, new_progress: int = 0):
    global tasks
    get_tasks()
    if new_progress == 0:
        if tasks[place_of_the_task-1]['progress'] == 'to do':
            tasks[place_of_the_task-1]['progress'] = 'in progress'
        elif tasks[place_of_the_task-1]['progress'] == 'in progress':
            tasks[place_of_the_task-1]['progress'] = 'done'
        elif tasks[place_of_the_task-1]['progress'] == 'done':
            print(f" The '{task_printable(place_of_the_task)}' is already done. You can delete it.")
            choice = input("Do you want to delete it? [y/n]").lower()
            if choice == 'y':
                delete_task(place_of_the_task)
    elif new_progress == 1:
        tasks[place_of_the_task-1]['progress'] = 'to do'
    elif new_progress == 2:
        tasks[place_of_the_task-1]['progress'] = 'in progress'
    elif new_progress == 3:
        tasks[place_of_the_task-1]['progress'] = 'done'
    else:
        print("Invalid progress.")
    set_tasks()

if __name__ == "__main__":
    while True:
        print()
        print("Task Tracker".center(30, "-"))
        print("Options:")
        print("1. Add new task")
        print("2. Delete task")
        print("3. List tasks")
        print("4. List tasks by status")
        print("5. Update task progress")
        print("6. Clear tasks")
        print("7. Exit")
        player_input = input("Enter your choice: ")
        if player_input == '1':
            add_task()
        elif player_input == '2':
            list_tasks()
            deleted_task = int(input("\nType the № of the task you want to delete: "))
            delete_task(deleted_task)
        elif player_input == '3':
            list_tasks()
        elif player_input == '4':
            which_tasks_to_list = input("Which tasks do you want to list?('to do', 'in progress', 'done'): ")
            list_tasks(which_tasks_to_list)
        elif player_input == '5':
            list_tasks()
            place_of_task = int(input("\nType the № of the task you want to update: "))
            new_prog = input("\nType the new progress(Skip that step if you want to just update it): ")
            if new_prog != '1' or new_prog != '2' or new_prog != '3':
                new_prog = '0'
            update_task(place_of_task, int(new_prog))
        elif player_input == '6':
            clear_tasks()
        elif player_input == '7':
            break
        else:
            print("Invalid input.")
        input("Press Enter to continue...")