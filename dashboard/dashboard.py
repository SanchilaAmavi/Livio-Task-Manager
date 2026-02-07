import streamlit as st
from modules import tasks
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌟 Livio – Task & Productivity Manager", layout="wide")
st.title("🌟 Livio – Task & Productivity Manager")
st.write("Livio is a modern, professional, and fully interactive task manager built with Python & Streamlit.")

# Load tasks
df = tasks.view_tasks()

# Sidebar: Add New Task
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

# Sidebar: Search Tasks
st.sidebar.header("🔍 Search Tasks")
search_keyword = st.sidebar.text_input("Search by title")
if st.sidebar.button("Search"):
    df = tasks.search_tasks(search_keyword)
    st.experimental_rerun()

# Main Dashboard
st.subheader("📋 Dashboard")
if df.empty:
    st.info("No tasks yet. Add your first task from the sidebar!")
else:
    # KPIs
    total_tasks = len(df)
    completed = len(df[df["Status"] == "Done"])
    pending = len(df[df["Status"] == "Pending"])
    in_progress = len(df[df["Status"] == "In Progress"])
    overdue = len(tasks.get_overdue_tasks())

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)
    col4.metric("In Progress", in_progress)
    col5.metric("Overdue", overdue)

    # Task table with color coding
    def priority_color(priority):
        if priority == "High":
            return "🔴 High"
        elif priority == "Medium":
            return "🟠 Medium"
        else:
            return "🟢 Low"

    for i, row in df.iterrows():
        # Highlight overdue tasks
        deadline_dt = datetime.strptime(row["Deadline"], "%Y-%m-%d").date()
        is_overdue = (deadline_dt < datetime.today().date()) and (row["Status"] != "Done")

        card_bg = "#FFCCCC" if is_overdue else "#F0F0F0"

        with st.container():
            st.markdown(f"<div style='padding:10px; background-color:{card_bg}; border-radius:5px'>", unsafe_allow_html=True)
            cols = st.columns([3,2,2,2,2])
            cols[0].write(row["Title"])
            cols[1].write(priority_color(row["Priority"]))
            cols[2].write(str(row["Deadline"]))
            # Status update dropdown
            new_status = cols[3].selectbox("Status", ["Pending", "In Progress", "Done"], index=["Pending","In Progress","Done"].index(row["Status"]), key=f"status_{i}")
            if cols[3].button("Update", key=f"update_{i}"):
                tasks.update_task(i, new_status)
                st.experimental_rerun()
            # Delete task
            if cols[4].button("❌ Delete", key=f"delete_{i}"):
                tasks.delete_task(i)
                st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Progress Bar
    st.subheader("📊 Task Completion Progress")
    completion = completed / total_tasks if total_tasks else 0
    st.progress(completion)

    # Optional: Chart
    st.subheader("📈 Task Status Chart")
    status_counts = df["Status"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(status_counts.index, status_counts.values, color=['orange','blue','green'])
    ax.set_ylabel("Number of Tasks")
    st.pyplot(fig)
