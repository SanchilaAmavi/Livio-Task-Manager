# modules/tasks.py

import pandas as pd
import os

# ---------------------------
# File path for tasks
# ---------------------------
TASK_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.csv")

# Ensure the data folder exists
if not os.path.exists(os.path.dirname(TASK_FILE)):
    os.makedirs(os.path.dirname(TASK_FILE))

# Ensure the CSV file exists
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["Title", "Priority", "Status", "Deadline"])
    df.to_csv(TASK_FILE, index=False)


# ---------------------------
# View tasks
# ---------------------------
def view_tasks():
    """Return all tasks as a DataFrame"""
    df = pd.read_csv(TASK_FILE)
    return df


# ---------------------------
# Add a new task
# ---------------------------
def add_task(title, priority, status, deadline):
    """Add a new task to the CSV"""
    df = pd.read_csv(TASK_FILE)
    new_task = {"Title": title, "Priority": priority, "Status": status, "Deadline": deadline}
    df = df.append(new_task, ignore_index=True)
    df.to_csv(TASK_FILE, index=False)


# ---------------------------
# Update task status
# ---------------------------
def update_task(title, new_status):
    """Update the status of a task"""
    df = pd.read_csv(TASK_FILE)
    df.loc[df["Title"] == title, "Status"] = new_status
    df.to_csv(TASK_FILE, index=False)


# ---------------------------
# Delete a task
# ---------------------------
def delete_task(title):
    """Delete a task from the CSV"""
    df = pd.read_csv(TASK_FILE)
    df = df[df["Title"] != title]
    df.to_csv(TASK_FILE, index=False)
