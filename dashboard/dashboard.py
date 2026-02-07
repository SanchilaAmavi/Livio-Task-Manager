# dashboard/dashboard.py
import streamlit as st
import pandas as pd
import sys, os
from datetime import datetime, timedelta

# --- Fix modules import ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from modules import tasks

# --- Page Config ---
st.set_page_config(page_title="🌟 Livio", layout="wide", page_icon="🌟")

# --- Sidebar Navigation ---
menu = ["Dashboard", "Tasks", "Calendar", "Statistics", "About"]
choice = st.sidebar.selectbox("Navigate", menu)

# --- Load tasks ---
df = tasks.view_tasks()
today = datetime.today().date()

# -------------------------
# DASHBOARD PAGE
# -------------------------
if choice == "Dashboard":
    st.title("🌟 Livio – Productivity Dashboard")
    
    total = len(df)
    done = len(df[df["Status"]=="Done"])
    pending = len(df[df["Status"]=="Pending"])
    overdue = len(df[pd.to_datetime(df["Deadline"], errors='coerce').dt.date < today])
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", total)
    col2.metric("Completed", done)
    col3.metric("Pending", pending)
    col4.metric("Overdue", overdue)
    
    # Task Cards with progress
    st.subheader("📋 Task Cards")
    if not df.empty:
        for i, row in df.iterrows():
            deadline = pd.to_datetime(row["Deadline"], errors='coerce').date()
            overdue_flag = deadline < today and row["Status"] != "Done"
            priority_color = "#d9534f" if row["Priority"]=="High" else "#f0ad4e" if row["Priority"]=="Medium" else "#5bc0de"
            status_color = "#5cb85c" if row["Status"]=="Done" else "#f0ad4e"
            card_bg = "#f8d7da" if overdue_flag else "#ffffff"
            
            progress_val = 100 if row["Status"]=="Done" else 0
            st.markdown(f"""
            <div style='background-color:{card_bg}; padding:15px; border-radius:10px; margin-bottom:10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1);'>
                <h4>{row["Title"]}</h4>
                <p>TaskID: {row["TaskID"]}</p>
                <p>Priority: <span style='color:{priority_color}'>{row["Priority"]}</span></p>
                <p>Deadline: {row["Deadline"]}</p>
                <p>Status: <span style='color:{status_color}'>{row["Status"]}</span></p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress_val)

    else:
        st.info("No tasks yet! Add tasks in the 'Tasks' page.")

# -------------------------
# TASKS PAGE
# -------------------------
elif choice == "Tasks":
    st.title("➕ Manage Your Tasks")
    
    # Add Task
    st.subheader("Add New Task")
    title = st.text_input("Task Title")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"], key="add_priority")
    deadline = st.date_input("Deadline", key="add_deadline")
    if st.button("Add Task"):
        if title:
            tasks.add_task(title, priority, str(deadline))
            st.success(f"Task '{title}' added!")
            st.experimental_rerun()
        else:
            st.warning("Enter a task title!")

    # Update Task
    if not df.empty:
        st.subheader("Update Task Status")
        task_id_update = st.number_input("Task ID to Update", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Pending", "Done"], key="update_status")
        if st.button("Update Task"):
            tasks.update_task(task_id_update, status=new_status)
            st.success(f"Task ID {task_id_update} updated!")
            st.experimental_rerun()

        # Delete Task
        st.subheader("Delete Task")
        task_id_delete = st.number_input("Task ID to Delete", min_value=1, step=1, key="delete")
        if st.button("Delete Task"):
            tasks.delete_task(task_id_delete)
            st.success(f"Task ID {task_id_delete} deleted!")
            st.experimental_rerun()

# -------------------------
# CALENDAR PAGE
# -------------------------
elif choice == "Calendar":
    st.title("📅 Calendar View")
    if df.empty:
        st.info("No tasks to display in calendar.")
    else:
        df["DeadlineDate"] = pd.to_datetime(df["Deadline"], errors='coerce')
        upcoming_dates = df[df["DeadlineDate"] >= pd.Timestamp(today)]
        if not upcoming_dates.empty:
            for date in sorted(upcoming_dates["DeadlineDate"].dt.date.unique()):
                st.markdown(f"### 📌 {date}")
                day_tasks = upcoming_dates[upcoming_dates["DeadlineDate"].dt.date == date]
                for _, row in day_tasks.iterrows():
                    st.write(f"- {row['Title']} ({row['Priority']}, {row['Status']})")
        else:
            st.info("No upcoming tasks.")

# -------------------------
# STATISTICS PAGE
# -------------------------
elif choice == "Statistics":
    st.title("📊 Productivity Statistics")
    if df.empty:
        st.info("No tasks yet! Add tasks to see stats.")
    else:
        st.subheader("Task Completion")
        st.bar_chart(df["Status"].value_counts())

        st.subheader("Tasks by Priority")
        st.bar_chart(df["Priority"].value_counts())

        st.subheader("Upcoming Deadlines (Next 7 Days)")
        upcoming = df[(df["DeadlineDate"] >= pd.Timestamp(today)) & 
                      (df["DeadlineDate"] <= pd.Timestamp(today + timedelta(days=7)))]
        if not upcoming.empty:
            st.table(upcoming[["TaskID", "Title", "Deadline", "Priority", "Status"]])
        else:
            st.info("No upcoming deadlines in the next 7 days.")

# -------------------------
# ABOUT PAGE
# -------------------------
elif choice == "About":
    st.title("ℹ️ About Livio")
    st.markdown("""
    **Livio** – Professional Task & Productivity Manager  

    Features:
    - Modern task cards with progress bars
    - Priority & status color coding
    - Overdue task highlighting
    - Calendar view of tasks
    - KPIs & charts for completion & priority
    - Interactive and professional UI  

    Built with **Python & Streamlit** as a portfolio-ready project. 🌟
    """)
