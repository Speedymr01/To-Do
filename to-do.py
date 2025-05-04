import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog  # For input dialogs
import json
import os
from datetime import datetime  # For date validation and comparison

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError):
            # Handle invalid JSON format
            messagebox.showwarning("File Error", f"Invalid format in {TASK_FILE}. Resetting tasks.")
            with open(TASK_FILE, "w") as file:
                json.dump([], file)  # Reset to an empty list
            return []
    else:
        # Create an empty file if it doesn't exist
        with open(TASK_FILE, "w") as file:
            json.dump([], file)
        return []

# Save tasks to file
def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

# Validate date format
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

# Add a new task
def add_task():
    task = task_entry.get().strip()
    if task:
        due_date = simpledialog.askstring("Due Date", "Enter due date (e.g., YYYY-MM-DD):")
        if due_date:
            valid_date = validate_date(due_date)
            if valid_date:
                tasks.append({"task": task, "due_date": due_date})
                save_tasks()
                update_task_lists()
                task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Invalid date format! Use YYYY-MM-DD.")
        else:
            messagebox.showwarning("Input Error", "Due date cannot be empty!")
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

# Remove selected task
def remove_task():
    selected_index = todo_listbox.curselection() or done_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        tasks.pop(selected_index)
        save_tasks()
        update_task_lists()
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

def update_task_lists():
    """Update both the 'To Do' and 'Done' listboxes."""
    todo_listbox.delete(0, tk.END)
    done_listbox.delete(0, tk.END)
    for index, task in enumerate(tasks):
        due_date = validate_date(task['due_date'])
        status = task.get("status", "TO DO")
        color = "#0288D1"  # Default blue for "TO DO"
        if status == "DONE":
            color = "#2F7D33"  # Green for "DONE"
            task_display = f"{task['task']:<30} {task['due_date']:<15}"
            done_listbox.insert(tk.END, task_display)
            done_listbox.itemconfig(done_listbox.size() - 1, {'bg': color, 'fg': 'white'})
            done_listbox.config(selectbackground=color, selectforeground="white")
        else:
            if due_date and due_date < datetime.now():
                color = "#D3302F"  # Red for "OVERDUE"
            task_display = f"{task['task']:<30} {task['due_date']:<15}"
            todo_listbox.insert(tk.END, task_display)
            todo_listbox.itemconfig(todo_listbox.size() - 1, {'bg': color, 'fg': 'white'})
            todo_listbox.config(selectbackground=color, selectforeground="white")

def toggle_task_status():
    """Toggle the status of the selected task and move it between listboxes."""
    selected_index = todo_listbox.curselection() or done_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if todo_listbox.curselection():
            task = tasks[selected_index]
            task["status"] = "DONE"
            save_tasks()
            update_task_lists()
            done_listbox.selection_set(done_listbox.size() - 1)  # Keep the task selected in the "Done" listbox
        elif done_listbox.curselection():
            task = tasks[selected_index]
            task["status"] = "TO DO"
            save_tasks()
            update_task_lists()
            todo_listbox.selection_set(todo_listbox.size() - 1)  # Keep the task selected in the "To Do" listbox

def on_select(event):
    """Update the button text based on the selected task's status."""
    selected_index = todo_listbox.curselection() or done_listbox.curselection()
    if selected_index:
        if todo_listbox.curselection():
            toggle_button.config(text="Mark as Done")
        elif done_listbox.curselection():
            toggle_button.config(text="Mark as To Do")

# Initialize tasks
tasks = load_tasks()

# Create the main window
root = tk.Tk()
root.title("To-Do Task Manager")

# Titles for the listboxes
todo_label = tk.Label(root, text="To Do", font=("Arial", 12, "bold"))
todo_label.grid(row=0, column=0, padx=10, pady=5)
done_label = tk.Label(root, text="Done", font=("Arial", 12, "bold"))
done_label.grid(row=0, column=1, padx=10, pady=5)

# "To Do" listbox
todo_listbox = tk.Listbox(
    root,
    width=50,
    height=15,
    selectforeground="white",  # Set the text color to white when selected
    selectbackground="white"   # Prevent default selection background color
)
todo_listbox.grid(row=1, column=0, padx=10, pady=10)

# "Done" listbox
done_listbox = tk.Listbox(
    root,
    width=50,
    height=15,
    selectforeground="white",  # Set the text color to white when selected
    selectbackground="white"   # Prevent default selection background color
)
done_listbox.grid(row=1, column=1, padx=10, pady=10)

# Bind the selection event to dynamically update the button text
todo_listbox.bind("<<ListboxSelect>>", on_select)
done_listbox.bind("<<ListboxSelect>>", on_select)

# Add task entry
task_entry = tk.Entry(root, width=40)
task_entry.grid(row=2, column=0, padx=10, pady=10)

# Add task button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=2, column=1, padx=10, pady=10)

# Remove task button
remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.grid(row=3, column=0, columnspan=2, pady=10)

# Toggle status button
toggle_button = tk.Button(root, text="", command=toggle_task_status)
toggle_button.grid(row=4, column=0, columnspan=2, pady=10)

# Populate the listboxes with tasks
update_task_lists()

# Run the application
root.mainloop()