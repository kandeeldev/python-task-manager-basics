"""
Task Manager Application
------------------------
Console-based task manager using SQLite for data storage.

Features:
- Add tasks (with optional notes)
- View all tasks
- Mark tasks as completed
- Rename tasks
- Remove tasks
- Persistent storage using SQLite database

Author: Ahmed Kandeel
Python Version: 3.10+
"""

import sqlite3

# =========================
# Database Setup
# =========================

db = sqlite3.connect("TaskManager.db")
cr = db.cursor()

cr.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    note TEXT
)
""")
db.commit()

# =========================
# Helper Functions
# =========================

def fetch_tasks(query, params=()):
    cr.execute(query, params)
    return cr.fetchall()


def choose_task(tasks, message):
    """
    Display tasks and allow user to choose one.
    Returns selected task id or None.
    """
    for i, task in enumerate(tasks, 1):
        print(f"{i}- {task[1]}")

    try:
        choice = int(input(message))
        if 1 <= choice <= len(tasks):
            return tasks[choice - 1][0]
    except ValueError:
        pass

    print("Invalid choice!")
    return None

# =========================
# Core Application Functions
# =========================

def add_task():
    task_name = input("Enter task name: ").strip().title()

    if not task_name or task_name.isdigit():
        print("Invalid task name!")
        return

    add_note = input("Do you want to add a note? (y/n): ").lower()
    note = None

    if add_note in ("y", "yes"):
        note = input("Enter note: ").strip().capitalize()

    cr.execute(
        "INSERT INTO tasks (task, completed, note) VALUES (?, ?, ?)",
        (task_name, 0, note)
    )
    db.commit()
    print("Task added successfully ✅")


def view_tasks():
    tasks = fetch_tasks("SELECT * FROM tasks")

    if not tasks:
        print("No tasks found!")
        return

    for i, task in enumerate(tasks, 1):
        status = "✔️" if task[2] == 1 else "❌"
        print(f"{i}- {task[1]} {status}")

        if task[3]:
            print(f"   📝 Note: {task[3]}")

    print("-" * 30)


def mark_task():
    """
    Mark only incomplete tasks as completed.
    We use a filtered list because completed tasks
    should not be selected again.
    """
    tasks = fetch_tasks(
        "SELECT * FROM tasks WHERE completed = 0"
    )

    if not tasks:
        print("No incomplete tasks!")
        return

    task_id = choose_task(
        tasks,
        "Choose completed task number: "
    )

    if task_id is None:
        return

    cr.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )
    db.commit()
    print("Task marked as completed 🎉")


def rename_task():
    tasks = fetch_tasks("SELECT * FROM tasks")

    if not tasks:
        print("No tasks to rename!")
        return

    task_id = choose_task(
        tasks,
        "Choose task to rename: "
    )

    if task_id is None:
        return

    new_name = input("Enter new task name: ").strip().title()
    if not new_name or new_name.isdigit():
        print("Invalid name!")
        return

    cr.execute(
        "UPDATE tasks SET task = ? WHERE id = ?",
        (new_name, task_id)
    )
    db.commit()
    print("Task renamed successfully ✏️")


def remove_task():
    tasks = fetch_tasks("SELECT * FROM tasks")

    if not tasks:
        print("No tasks to remove!")
        return

    task_id = choose_task(
        tasks,
        "Choose task to remove: "
    )

    if task_id is None:
        return

    cr.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    db.commit()
    print("Task removed successfully 🗑️")

# =========================
# Main Application Loop
# =========================

def main():
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
            add_task()
        elif choice == "2":
            mark_task()
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            remove_task()
        elif choice == "5":
            rename_task()
        elif choice == "6":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()