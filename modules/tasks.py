import os
import pandas as pd

# ✅ Ensure data folder exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ✅ CSV file path
TASK_FILE = os.path.join(DATA_DIR, "tasks.csv")

# ✅ Create tasks.csv if it doesn't exist
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["Title", "Priority", "Deadline", "Status"])
    df.to_csv(TASK_FILE, index=False)
else:
    df = pd.read_csv(TASK_FILE)

# Function to add a task
def add_task(title, priority, deadline, status="Pending"):
    global df
    new_task = {"Title": title, "Priority": priority, "Deadline": deadline, "Status": status}
    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
    df.to_csv(TASK_FILE, index=False)

# Function to update task status
def update_task(index, status):
    global df
    df.loc[index, "Status"] = status
    df.to_csv(TASK_FILE, index=False)

# Function to delete a task
def delete_task(index):
    global df
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(TASK_FILE, index=False)

# ✅ Function to view tasks (add this at the bottom of tasks.py)

def view_tasks():
    """Return the current dataframe of tasks"""
    global df
    return df
