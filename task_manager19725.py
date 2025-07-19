import time
import uuid
import json
from datetime import datetime

print("\n" + "=" * 35)
print("         /// TASK MANAGER ///        ")
print("=" * 35 + "\n")

class Task:
    def __init__(self, task_name, status="pending", task_id=None):
        self.task_id = task_id if task_id else str(uuid.uuid4())[:8]
        self.task_name = task_name
        self.status = status
        self.created_at = datetime.now().strftime("%I:%M:%S | %d-%m-%Y")

    def __str__(self):
        return (f"Task ID      : {self.task_id}\n"
                f"Task Name    : {self.task_name}\n"
                f"Status       : {self.status}\n"
                f"Created At   : {self.created_at}\n")

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "status": self.status,
            "created_at": self.created_at
        }


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, status="pending"):
        task = Task(name, status)
        self.tasks.append(task)
        print(f"> Task '{name}' added successfully!")

    def remove_task(self, id_or_name):
        for task in self.tasks:
            if task.task_id == id_or_name or task.task_name == id_or_name:
                self.tasks.remove(task)
                print(f"> Task '{task.task_name}' deleted successfully!")
                return
        print("> No matching task found!")

    def update_task(self, task_id, new_name=None, new_status=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if new_name:
                    task.task_name = new_name
                if new_status:
                    task.status = new_status
                print("> Task updated successfully!")
                return
        print(f"> No task found with ID '{task_id}'")

    def view_tasks(self):
        if not self.tasks:
            print("> No tasks available.")
            return
        print("\n======= CURRENT TASKS =======")
        for task in self.tasks:
            print("-" * 30)
            print(task)
        print(f"== Total Tasks: {len(self.tasks)} ==")

    def save_tasks(self, filename="data_saver.json"):
        if not self.tasks:
            print("> No tasks to save.")
            return
        with open(filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
        print("> Tasks saved to JSON successfully!")

    def load_tasks(self, filename="data_saver.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    task = Task(
                        task_name=item['task_name'],
                        status=item['status'],
                        task_id=item['task_id']
                    )
                    self.tasks.append(task)
            print("> Tasks loaded from file successfully!")
        except FileNotFoundError:
            print("> No saved data found.")


# 🧪 Command-line UI (simple CLI loop)
if __name__ == "__main__":
    tm = TaskManager()
    tm.load_tasks()

    while True:
        print("\n[1] Add Task | [2] Remove Task | [3] Update Task")
        print("[4] View Tasks | [5] Save Tasks | [6] Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter task name: ")
            status = input("Enter task status (pending/completed): ")
            tm.add_task(name, status)

        elif choice == "2":
            id_or_name = input("Enter Task ID or Name to delete: ")
            tm.remove_task(id_or_name)

        elif choice == "3":
            task_id = input("Enter Task ID to update: ")
            new_name = input("New name (or leave blank): ").strip()
            new_status = input("New status (or leave blank): ").strip()
            tm.update_task(task_id, new_name if new_name else None, new_status if new_status else None)

        elif choice == "4":
            tm.view_tasks()

        elif choice == "5":
            tm.save_tasks()

        elif choice == "6":
            print("Goodbye, King Trillionare 👑.")
            break

        else:
            print("> Invalid choice. Please try again.")
