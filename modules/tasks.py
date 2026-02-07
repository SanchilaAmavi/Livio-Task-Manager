import os
import pandas as pd

# Ensure data folder exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

TASK_FILE = os.path.join(DATA_DIR, "tasks.csv")

# Create CSV if it doesn't exist
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["Title", "Priority", "Deadline", "Status"])
    df.to_csv(TASK_FILE, index=False)
else:
    df = pd.read_csv(TASK_FILE)

# Add a task
def add_task(title, priority, deadline, status="Pending"):
    global df
    new_task = {"Title": title, "Priority": priority, "Deadline": deadline, "Status": status}
    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
    df.to_csv(TASK_FILE, index=False)

# Update task status
def update_task(index, status):
    global df
    df.loc[index, "Status"] = status
    df.to_csv(TASK_FILE, index=False)

# Delete task
def delete_task(index):
    global df
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(TASK_FILE, index=False)

# ✅ MUST BE AT THE BOTTOM
def view_tasks():
    global df
    return df
