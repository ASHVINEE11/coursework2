from google import genai
import streamlit as st
user_Q = ""
while user_Q != "quit":
    user_Q = str(input("Please enter your fav question: "))
    # client = genai.Client(api_key= st.secrets["GEMINI_API_KEY"])
    client = genai.Client(api_key= "AIzaSyBeevile3ltgltEbVrb0kwN-JkS465gx2U")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=user_Q)
    print(response.text)
    if user_Q == "quit":
        print("bye")
        breakpoint()
        