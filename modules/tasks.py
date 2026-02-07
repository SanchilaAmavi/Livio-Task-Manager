# modules/tasks.py
import pandas as pd
import os

# --- Set up project paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
TASK_FILE = os.path.join(DATA_FOLDER, "tasks.csv")

# --- Create data folder if it doesn't exist ---
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Initialize CSV if it doesn't exist ---
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["TaskID", "Title", "Priority", "Deadline", "Status"])
    df.to_csv(TASK_FILE, index=False)
else:
    df = pd.read_csv(TASK_FILE)

# --- Task Functions ---

def add_task(title, priority, deadline):
    """
    Add a new task.
    """
    global df
    task_id = len(df) + 1
    new_task = {
        "TaskID": task_id,
        "Title": title,
        "Priority": priority,
        "Deadline": deadline,
        "Status": "Pending"
    }
    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
    df.to_csv(TASK_FILE, index=False)
    print(f"Task '{title}' added successfully!")

def update_task(task_id, title=None, priority=None, deadline=None, status=None):
    """
    Update an existing task by TaskID.
    """
    global df
    if task_id in df["TaskID"].values:
        idx = df[df["TaskID"] == task_id].index[0]
        if title: df.at[idx, "Title"] = title
        if priority: df.at[idx, "Priority"] = priority
        if deadline: df.at[idx, "Deadline"] = deadline
        if status: df.at[idx, "Status"] = status
        df.to_csv(TASK_FILE, index=False)
        print(f"Task ID {task_id} updated successfully!")
    else:
        print(f"Task ID {task_id} not found.")

def delete_task(task_id):
    """
    Delete a task by TaskID.
    """
    global df
    if task_id in df["TaskID"].values:
        df = df[df["TaskID"] != task_id]
        df.to_csv(TASK_FILE, index=False)
        print(f"Task ID {task_id} deleted successfully!")
    else:
        print(f"Task ID {task_id} not found.")

def view_tasks():
    """
    Return current tasks as a DataFrame.
    """
    global df
    return df
