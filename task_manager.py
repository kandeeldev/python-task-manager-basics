"""
Task Manager Application
------------------------
A simple console-based task manager using JSON for data storage.

Features:
- Add tasks (with optional notes)
- View all tasks
- Mark tasks as completed
- Rename tasks
- Remove tasks
- Persistent storage using JSON

Author: Ahmed Kandeel
"""

import json

FILE_NAME = "Tasks.json"


# =========================
# File Handling Functions
# =========================

def save_tasks(tasks):
    """Save tasks list to JSON file"""
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
    """Load tasks from JSON file if exists"""
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# =========================
# Helper Functions
# =========================

def choose_task(tasks, message):
    """
    Display tasks and allow user to choose one
    Returns index of selected task or None
    """
    for i, task in enumerate(tasks, 1):
        print(f"{i}- {task['task']}")

    try:
        choice = int(input(message))
        if 1 <= choice <= len(tasks):
            return choice - 1
    except ValueError:
        pass

    print("Invalid choice!")
    return None


# =========================
# Core Application Functions
# =========================

def add_task(tasks):
    """Add a new task"""
    task_name = input("Enter task name: ").strip().title()

    if not task_name:
        print("Task cannot be empty!")
        return

    if task_name.isdigit():
        print("Task name must be text!")
        return

    add_note = input("Do you want to add a note? (y/n): ").lower()
    task_data = {
        "task": task_name,
        "completed": False
    }

    if add_note in ("y", "yes"):
        note = input("Enter note: ").strip().capitalize()
        task_data["note"] = note

    tasks.append(task_data)
    save_tasks(tasks)
    print("Task added successfully ✅")


def view_tasks(tasks):
    """Display all tasks"""
    if not tasks:
        print("No tasks to display.")
        return

    for i, task in enumerate(tasks, 1):
        status = "✔️" if task["completed"] else "❌"
        print(f"{i}. {task['task']} {status}")

        if "note" in task:
            print(f"   📝 Note: {task['note']}")

    print("-" * 30)


def mark_task(tasks):
    """Mark a task as completed"""

    # NOTE:
    # Modifying incomplete_tasks updates the original task objects
    # because they reference the same dictionaries
    incomplete_tasks = [task for task in tasks if not task["completed"]]

    if not incomplete_tasks:
        print("No incomplete tasks.")
        return

    index = choose_task(incomplete_tasks, "Choose completed task number: ")
    if index is None:
        return

    incomplete_tasks[index]["completed"] = True
    save_tasks(tasks)
    print("Task marked as completed 🎉")


def rename_task(tasks):
    """Rename an existing task"""
    if not tasks:
        print("No tasks to rename.")
        return

    index = choose_task(tasks, "Choose task number to rename: ")
    if index is None:
        return

    new_name = input("Enter new task name: ").strip().title()

    if not new_name or new_name.isdigit():
        print("Invalid task name!")
        return

    tasks[index]["task"] = new_name
    save_tasks(tasks)
    print("Task renamed successfully ✏️")


def remove_task(tasks):
    """Remove a task"""
    if not tasks:
        print("No tasks to remove.")
        return

    index = choose_task(tasks, "Choose task number to remove: ")
    if index is None:
        return

    removed_task = tasks.pop(index)
    save_tasks(tasks)
    print(f"Task '{removed_task['task']}' removed successfully 🗑️")


# =========================
# Main Application Loop
# =========================

def main():
    tasks = load_tasks()

    print("Welcome to Task Manager 👋")

    while True:
        print("""
1- Add Task
2- Mark Task as Completed
3- View Tasks
4- Remove Task
5- Rename Task
6- Quit
        """)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            mark_task(tasks)
        elif choice == "3":
            view_tasks(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            rename_task(tasks)
        elif choice == "6":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice, please try again!")


if __name__ == "__main__":
    main()