"""
Task Manager Application
------------------------
Object-Oriented task manager using JSON for data storage.

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


class TaskManager:
    FILE_NAME = "Tasks.json"

    def __init__(self):
        self.tasks = self.load_tasks()

    # =========================
    # File Handling
    # =========================

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open(self.FILE_NAME, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    # =========================
    # Helper Methods
    # =========================

    def choose_task(self, tasks, message):
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
    # Core Methods
    # =========================

    def add_task(self):
        task_name = input("Enter task name: ").strip().title()

        if not task_name or task_name.isdigit():
            print("Invalid task name!")
            return

        task_data = {
            "task": task_name,
            "completed": False
        }

        add_note = input("Do you want to add a note? (y/n): ").lower()
        if add_note in ("y", "yes"):
            note = input("Enter note: ").strip().capitalize()
            task_data["note"] = note

        self.tasks.append(task_data)
        self.save_tasks()
        print("Task added successfully ✅")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found!")
            return

        for i, task in enumerate(self.tasks, 1):
            status = "✔️" if task["completed"] else "❌"
            print(f"{i}. {task['task']} {status}")

            if "note" in task:
                print(f"   📝 Note: {task['note']}")

        print("-" * 30)

    def mark_task(self):
        """
        Mark only incomplete tasks as completed.
        We use a filtered list but modify the original task objects.
        """
        incomplete_tasks = [
            task for task in self.tasks if not task["completed"]
        ]

        if not incomplete_tasks:
            print("No incomplete tasks!")
            return

        index = self.choose_task(
            incomplete_tasks,
            "Choose completed task number: "
        )

        if index is None:
            return

        incomplete_tasks[index]["completed"] = True
        self.save_tasks()
        print("Task marked as completed 🎉")

    def rename_task(self):
        if not self.tasks:
            print("No tasks to rename!")
            return

        index = self.choose_task(
            self.tasks,
            "Choose task to rename: "
        )

        if index is None:
            return

        new_name = input("Enter new task name: ").strip().title()
        if not new_name or new_name.isdigit():
            print("Invalid name!")
            return

        self.tasks[index]["task"] = new_name
        self.save_tasks()
        print("Task renamed successfully ✏️")

    def remove_task(self):
        if not self.tasks:
            print("No tasks to remove!")
            return

        index = self.choose_task(
            self.tasks,
            "Choose task to remove: "
        )

        if index is None:
            return

        removed = self.tasks.pop(index)
        self.save_tasks()
        print(f"Task '{removed['task']}' removed successfully 🗑️")

    # =========================
    # Application Runner
    # =========================

    def run(self):
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
                self.add_task()
            elif choice == "2":
                self.mark_task()
            elif choice == "3":
                self.view_tasks()
            elif choice == "4":
                self.remove_task()
            elif choice == "5":
                self.rename_task()
            elif choice == "6":
                print("Goodbye 👋")
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    app = TaskManager()
    app.run()