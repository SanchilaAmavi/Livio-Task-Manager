import streamlit as st
from modules import tasks
import pandas as pd

st.set_page_config(page_title="🌟 Livio – Task & Productivity Manager", layout="wide")

st.title("🌟 Livio – Task & Productivity Manager")

# Load tasks
df = tasks.view_tasks()

# Sidebar: Add new task
st.sidebar.header("➕ Add New Task")
title = st.sidebar.text_input("Task Title")
priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])
deadline = st.sidebar.date_input("Deadline")

if st.sidebar.button("Add Task"):
    if title:
        tasks.add_task(title, priority, deadline)
        st.experimental_rerun()
    else:
        st.sidebar.error("Task title cannot be empty!")

# Main dashboard
st.subheader("📋 Dashboard")

if df.empty:
    st.info("No tasks yet. Add your first task from the sidebar!")
else:
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
        col1.write(row["Title"])
        col2.write(row["Priority"])
        col3.write(str(row["Deadline"]))
        col4.write(row["Status"])

        # Update Status
        new_status = col4.selectbox("Change Status", ["Pending", "In Progress", "Done"], index=["Pending", "In Progress", "Done"].index(row["Status"]), key=f"status_{i}")
        if col4.button("Update", key=f"update_{i}"):
            tasks.update_task(i, new_status)
            st.experimental_rerun()

        # Delete Task
        if col5.button("❌ Delete", key=f"delete_{i}"):
            tasks.delete_task(i)
            st.experimental_rerun()
