import streamlit as st
import pandas as pd
import os

# Login check

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Login.py")
    st.stop()

st.set_page_config(page_title="Data Governance Dashboard", layout="wide")

st.title("🌐 Data Governance & Discovery Dashboard")
st.markdown('---')


# Load datasets_metadata csv
st.subheader("🗂️ Dataset Catalog")

csv_path = r"C:\Users\ashvi\OneDrive - Middlesex University\Desktop\CW2 CST1510\CW2_M01070954_CST1510\DATA\datasets_metadata.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"{len(df)} datasets loaded from CSV")
else:
    st.error("Could not load CSV")
    df = pd.DataFrame({
        'name': ['Sample1', 'Sample2'],
        'rows': [1000, 2000],
        'columns': [10, 20],
        'uploaded_by': ['IT', 'Cyber']
    })

st.dataframe(df, use_container_width=True)

st.markdown("----")


# Bar chart 1 (Dataset Size)

st.subheader("📦 Dataset Size (Rows per Dataset)")

if "rows" in df.columns:
    size_counts = df[["name", "rows"]].set_index("name")
    st.bar_chart(size_counts)
else:
    st.info("No 'rows' column found in dataset.")


#  Metrics

st.subheader("Data Overview 📈")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Datasets", df.shape[0])

with col2:
    st.metric("Total Rows", df["rows"].sum() if "rows" in df else 0)

with col3:
    st.metric("Average Columns", round(df["columns"].mean(), 2) if "columns" in df else 0)

st.markdown("----")


# Sidebar Filters

with st.sidebar:
    st.header("🔍 Filters")

    if "uploaded_by" in df.columns:
        selected = st.selectbox("Filter by uploader", df["uploaded_by"].unique())
        filtered = df[df["uploaded_by"] == selected]
        st.caption(f"Showing {len(filtered)} datasets uploaded by {selected}")
    else:
        filtered = df
        st.caption(f"Showing all {len(filtered)} datasets")

    st.markdown("---")

# ✅ Filtered Charts

st.subheader("Filtered Charts")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Rows per Dataset**")
    if "rows" in filtered.columns:
        st.bar_chart(filtered.set_index("name")["rows"])
    else:
        st.info("No 'rows' column found.")

with chart_col2:
    st.write("**Columns per Dataset**")
    if "columns" in filtered.columns:
        st.bar_chart(filtered.set_index("name")["columns"])
    else:
        st.info("No 'columns' column found.")

st.markdown("---")

#  Governance Recommendations

st.subheader("✅ Governance & Archiving Recommendations")

for _, row in df.iterrows():
    name = row["name"]
    rows_count = row["rows"]

    if rows_count > 500000:
        st.warning(f"📌 {name}: Very large dataset → Recommend archiving or compressing older partitions.")
    elif rows_count > 100000:
        st.info(f"📌 {name}: Medium dataset → Review retention policy.")
    else:
        st.success(f"📌 {name}: Small dataset → No immediate action required.")

st.markdown("---")


#  Navigation

st.subheader("🔀 Navigate")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Back to IT Operations Dashboard"):
        st.switch_page("pages/2_IT_Operations.py")

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