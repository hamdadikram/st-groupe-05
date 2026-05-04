"""
Todo List Manager
=================
A simple command-line todo list manager for project management.
Data is saved locally in a JSON file.

Usage:
    python todo_list.py
"""

import json
import os
from datetime import datetime


TODO_FILE = "todos.json"


def load_todos():
    """Load todos from JSON file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(todos, title, priority="medium"):
    """Add a new todo item."""
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "done": False,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"✅ Added: [{todo['id']}] {title} (Priority: {priority})")


def list_todos(todos, show_done=True):
    """Display all todos."""
    if not todos:
        print("📋 No tasks found. Add one with option 1!")
        return

    print("\n" + "=" * 50)
    print("         📝 TODO LIST")
    print("=" * 50)

    pending = [t for t in todos if not t["done"]]
    done = [t for t in todos if t["done"]]

    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    if pending:
        print("\n🔲 PENDING:")
        for todo in pending:
            icon = priority_icon.get(todo.get("priority", "medium"), "🟡")
            print(f"  [{todo['id']}] {icon} {todo['title']}")
            print(f"       Created: {todo.get('created_at', 'N/A')}")

    if show_done and done:
        print("\n✅ COMPLETED:")
        for todo in done:
            print(f"  [{todo['id']}] ✔  {todo['title']}")

    print("=" * 50)
    print(f"Total: {len(todos)} | Pending: {len(pending)} | Done: {len(done)}\n")


def complete_todo(todos, todo_id):
    """Mark a todo as completed."""
    for todo in todos:
        if todo["id"] == todo_id:
            if todo["done"]:
                print(f"⚠️  Task [{todo_id}] is already completed.")
            else:
                todo["done"] = True
                save_todos(todos)
                print(f"✅ Completed: [{todo_id}] {todo['title']}")
            return
    print(f"❌ Task with ID {todo_id} not found.")


def delete_todo(todos, todo_id):
    """Delete a todo by ID."""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"🗑️  Deleted: [{todo_id}] {removed['title']}")
            return
    print(f"❌ Task with ID {todo_id} not found.")


def clear_completed(todos):
    """Remove all completed todos."""
    before = len(todos)
    todos[:] = [t for t in todos if not t["done"]]
    after = len(todos)
    save_todos(todos)
    print(f"🧹 Cleared {before - after} completed task(s).")


def get_int_input(prompt):
    """Safely get an integer input from the user."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("⚠️  Please enter a valid number.")
        return None


def main():
    """Main loop for the Todo List CLI app."""
    todos = load_todos()

    print("\n🚀 Welcome to Todo List Manager!")
    print("   Your tasks are saved in:", os.path.abspath(TODO_FILE))

    while True:
        print("\n--- MENU ---")
        print("1. ➕ Add task")
        print("2. 📋 View all tasks")
        print("3. ✅ Mark task as done")
        print("4. 🗑️  Delete task")
        print("5. 🧹 Clear completed tasks")
        print("6. 🚪 Exit")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("⚠️  Title cannot be empty.")
                continue
            print("Priority: (1) High  (2) Medium  (3) Low")
            p_choice = input("Choose priority [default: 2]: ").strip()
            priority_map = {"1": "high", "2": "medium", "3": "low"}
            priority = priority_map.get(p_choice, "medium")
            add_todo(todos, title, priority)

        elif choice == "2":
            list_todos(todos)

        elif choice == "3":
            list_todos(todos, show_done=False)
            todo_id = get_int_input("Enter task ID to mark as done: ")
            if todo_id:
                complete_todo(todos, todo_id)

        elif choice == "4":
            list_todos(todos)
            todo_id = get_int_input("Enter task ID to delete: ")
            if todo_id:
                confirm = input(f"Are you sure you want to delete task [{todo_id}]? (y/n): ").strip().lower()
                if confirm == "y":
                    delete_todo(todos, todo_id)

        elif choice == "5":
            clear_completed(todos)

        elif choice == "6":
            print("\n👋 Goodbye! Keep crushing your tasks! 💪\n")
            break

        else:
            print("⚠️  Invalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()
