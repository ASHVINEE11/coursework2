import streamlit as st
import pandas as pd
import os


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    #st.error("Please login first 🔒")
    #if st.button("Go to login"):
        st.switch_page("Login.py")
        st.stop() 

st.set_page_config(page_title="IT Operations Dashboard", layout="wide")

st.title("🎟️ IT Tickets Dashboard")
st.markdown('---')

# CSV loading
st.subheader(" 🗂️ Raw Ticket Data")
csv_path = r"C:\Users\ashvi\OneDrive - Middlesex University\Desktop\CW2 CST1510\CW2_M01070954_CST1510\DATA\it_tickets(1).csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"{len(df)} rows loaded from CSV")
else:
    st.error("Could not load CSV")

    df = pd.DataFrame({
        'priority' : ['High', 'Medium', 'Low', 'Critical'],
        'status': ['Open', 'Waiting for User', 'Resolved', 'In Progress']
    })
st.dataframe(df, use_container_width= True)

st.markdown("----")



# Bar chart 1
st.subheader("🚩 Tickets by priority")
severity_counts = df["priority"].value_counts().reset_index()
severity_counts.columns= ["priority", "count"]
st.bar_chart(severity_counts.set_index("priority"))



# Metrics
st.subheader("Data overview 📈")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Critical Tickets", df[df["priority"] == "Critical"].shape[0])

with col2:
    st.metric("Total Tickets",df.shape[0])

with col3:
    st.metric("Avg Resolution time (Hours)", df["resolution_time_hours"].mean())


st.markdown("----")

# Apply sidebar
with st.sidebar:
    st.header("🔍 Filters")
    if "priority" in df.columns:
        selected = st.selectbox("Filter by priority", df["priority"].unique())
        
        filtered = df[df["priority"] == selected]
        st.caption(f"Showing {len(filtered)} tickets with priority = {selected}")
    else:
        filtered = df
        st.caption(f"Showing all {len(filtered)} tickets")

    st.markdown("---")
    

st.subheader("Filtered bar charts")

# filtered charts.

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Average Resolution time by staff**")
    if "assigned_to" in filtered.columns and "resolution_time_hours" in filtered.columns:
        st.bar_chart(filtered.groupby("assigned_to")["resolution_time_hours"].mean())
    else:
        st.info("No such data")

with chart_col2:
    st.write("**Tickets by status**")
    if "status" in filtered.columns:
        st.bar_chart(filtered.groupby("status")["resolution_time_hours"].mean())
    else:
        st.info("No status column")

st.markdown("---")

st.subheader("🔀 Navigate")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(" 📊 Back to Cybersecurity Dashboard"):
        st.switch_page("pages/1_Cybersecurity.py")

with col2:
    if st.button("🤖 AI Analyser"):
        st.switch_page("pages/3_AI_Analyzer.py")

with col3:
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("You have been logged out")
        st.switch_page("Login.py")
        st.rerun()



    

