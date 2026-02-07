import os
import pandas as pd

# Make sure the data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Path to tasks file
TASK_FILE = os.path.join("data", "tasks.csv")

# If tasks.csv does not exist, create it
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["Title", "Priority", "Deadline", "Status"])
    df.to_csv(TASK_FILE, index=False)

# Now you can safely read/write tasks
df = pd.read_csv(TASK_FILE)
