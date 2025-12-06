import streamlit as st
import pandas as pd
import os


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    #st.error("Please login first 🔒")
    #if st.button("Go to login"):
        st.switch_page("app.py")
        st.stop() 

st.set_page_config(page_title="Cyber Security Dashboard", layout="wide")

st.title("📊 Cyber Security Dashboard")
st.write("Welcome!")
st.markdown('---')

# CSV loading
st.subheader("Raw Data")
csv_path = r"C:\Users\ashvi\OneDrive - Middlesex University\Desktop\CW2 CST1510\CW2_M01070954_CST1510\DATA\cyber_incidents_csv.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"{len(df)} rows loaded from CSV")
else:
    st.error("Could not load CSV")

    df = pd.DataFrame({
        'severity' : ['High', 'Medium', 'Low', 'Critical'],
        'status': ['Open', 'Closed', 'Resolved', 'In Progress']
    })
st.dataframe(df, use_container_width= True)

st.markdown("----")



# Bar chart 1
st.subheader("🚩 Incidents by severity")
severity_counts = df["severity"].value_counts().reset_index()
severity_counts.columns= ["severity", "count"]
st.bar_chart(severity_counts.set_index("severity"))



# Metrics
st.subheader("Data overview 📈")

col1, col2 = st.columns(2)

with col1:
    st.metric("High", df[df["severity"] == "High"].shape[0])

with col2:
    st.metric("Incidents",df.shape[0])


# Apply sidebar
with st.sidebar:
    st.header("🔍 Filters")
    if "severity" in df.columns:
        selected = st.selectbox("Severity", df["severity"].unique())
        
        filtered = df[df["severity"] == selected]
        st.caption(f"Showing {len(filtered)} rows with severity = {selected}")
    else:
        filtered = df
        st.caption(f"Showing all {len(filtered)} rows")

    st.markdown("---")
    

st.subheader("Filtered bar charts")

# filtered charts.
col1, col2 = st.columns(2)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Incidents by severity**")
    if "severity" in filtered.columns:
        st.bar_chart(filtered["severity"].value_counts())
    else:
        st.info("No severity data")

with chart_col2:
    st.write("**Incidents by status**")
    if "status" in filtered.columns:
        st.bar_chart(filtered["status"].value_counts())
    else:
        st.info("No status column")

# Add incidents
st.markdown("## Add Incidents ##")
with st.form("Add new incident"):
    date = st.date_input("enter a date")
    category = st.selectbox("Category", ["Malware", "Phishing", "DDoS", "Misconfiguration"])
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed", "Resolved", "In Progress"])
    description = st.text_input("Description")
    submitted = st.form_submit_button("Submit")

if submitted:
    new_incident = {
        "date": date,
        "category": category,
        "severity" : severity,
        "status": status,
        "description": description,   
    }
    st.success("✅️ Incident added!")
    st.write(new_incident)
    st.rerun()

# Log out button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out")
    st.switch_page("app.py")
    st.rerun()


    

