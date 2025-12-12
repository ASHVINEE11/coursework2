import streamlit as st
from google import genai
from google.genai import types
import sys
import os
import pandas as pd

# Added this since i was getting no module found error.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0,PROJECT_ROOT)

from app.data.incidents import get_all_incidents

# Initialise Gemini Client
client = genai.Client(api_key= st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title = "AI ANALYSER", layout="wide")

st.title("🤖  AI Analyzer")
st.write("Switch between Cyber incidents and IT tickets below.")
st.markdown("----")

# Tabs for easy navigation.
tab1, tab2 = st.tabs(["📊 Cyber Incidents", "🎟️ IT Tickets"])

# Cyber incidents AI Analyser.

with tab1:
    st.header("AI Incident Analyzer")

    incidents = get_all_incidents()
    if not incidents.empty:
        incidents_options = [
        f"{row['category']} - {row['severity']}"
        for _, row in incidents.iterrows()
    ]

    selected_idx = st.selectbox(
        "Select incident to analyse:",
        list(range(len(incidents))),
        format_func=lambda i: incidents_options[i]
    )

    incident =  incidents.iloc[int(selected_idx)]

# Display incident details
    st.subheader("Incident Details")
    st.write(f"*Category:* {incident['category']}")
    st.write(f"*Severity:* {incident['severity']}")
    st.write(f"*Description:* {incident['description']}")   
    st.write(f"*Status:* {incident['status']}")

    if st.button("Analyse with AI", type="primary", key="analyse_incident"):
    
        with st.spinner("AI analyzing incident...."):
        # Create analysis prompt
            analysis_prompt = f"""Analyse this cybersecurity incident:
            severity: {incident['severity']}
            Description: {incident['description']}
            status: {incident['status']}


        provide:
        1. Root cause analysis
        2. Immediate actions needed
        3. Long-term prevention measures
        4. Risk assessment"""
        # Call Gemini API
        response = client.models.generate_content_stream(
            model = "gemini-2.5-flash",
            config= types.GenerateContentConfig(
                system_instruction= "You are a cybersecurity expert."
            ),
            contents={"role": "user", "parts": [{"text": analysis_prompt}]},
        )

        # Display Ai analysis
        st.subheader(" AI Analysis")
        container = st.empty()
        full_reply = ""
        for chunk in response:
            full_reply += chunk.text
            container.markdown(full_reply)
            
        else:
            st.warning("No information found on database.")


# IT Operations Analayser

from app.data.tickets import get_all_tickets

with tab2:
    st.header("IT OPERATIONS Analyzer")

    tickets = get_all_tickets()
    if not tickets.empty:
        tickets_options = [
        f"{row['priority']} - {row['status']}"
        for _, row in tickets.iterrows()
    ]

    selected_idx = st.selectbox(
        "Select tickets to analyse:",
        list(range(len(tickets))),
        format_func=lambda i: tickets_options[i]
    )
    if selected_idx is not None:
        ticket =  tickets.iloc[int(selected_idx)]

# Display incident details
        st.subheader("Ticket Details")
        st.write(f"*Ticket ID:* {ticket['ticket_id']}")
        st.write(f"*Priority:* {ticket['priority']}")
        st.write(f"*Assigned to:* {ticket['assigned_to']}")
        st.write(f"*Description:* {ticket['description']}")
        st.write(f"*Status:* {ticket['status']}")
        st.write(f"*Resolution time (hours):* {ticket['resolution_time_hours']}")
    else:
        st.info("Please select a ticket to analyse.")

    if st.button("Analyse with AI", type="primary", key="analyse_ticket"):
        with st.spinner("AI analyzing ticket...."):
        # Create analysis prompt
            analysis_prompt = f"""Analyse this IT ticket:
            Ticket ID: {ticket['ticket_id']}
            priority: {ticket['priority']}
            Description: {ticket['description']}
            status: {ticket['status']}
            Resolution Time (hours): {ticket['resolution_time_hours']}


        provide:
        1. Root cause analysis of delays
        2. Immediate actions needed to speed up delays
        3. Long-term process improvements
        4. Risk assessment
        5. Comment on the resolution time
        """
        
        # Call Gemini API
        response = client.models.generate_content_stream(
            model = "gemini-1.5-flash", 
            config= types.GenerateContentConfig(
                system_instruction= "You are an IT support expert."
            ),
            contents={"role": "user", "parts": [{"text": analysis_prompt}]},
        )

        # Display Ai analysis
        st.subheader(" AI Analysis")
        container = st.empty()
        full_reply = ""
        for chunk in response:
            full_reply += chunk.text
            container.markdown(full_reply)
            
    else:
            st.warning("No information found on database.")

