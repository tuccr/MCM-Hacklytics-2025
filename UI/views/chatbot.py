import random
import time
import pandas as pd
import streamlit as st

import query


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hey there! Need help? Check out my fun YouTube channel 'CodingIsFun': https://youtube.com/@codingisfun!",
            "Hi! What's up? Don't forget to subscribe to 'CodingIsFun': https://youtube.com/@codingisfun!",
            "Hello! Need assistance? My YouTube channel 'CodingIsFun' is full of great tips: https://youtube.com/@codingisfun!",
            "Hey! Got a question? Also, subscribe to 'CodingIsFun' for awesome tutorials: https://youtube.com/@codingisfun!",
            "Hi there! How can I help? BTW, my channel 'CodingIsFun' is super cool: https://youtube.com/@codingisfun!",
            "Hello! Looking for help? Check out 'CodingIsFun' on YouTube: https://youtube.com/@codingisfun!",
            "Hey! Need assistance? 'CodingIsFun' YouTube channel has you covered: https://youtube.com/@codingisfun!",
            "Hi! Got any coding questions? Don't forget to watch 'CodingIsFun': https://youtube.com/@codingisfun!",
            "Hello! Need help? 'CodingIsFun' on YouTube is a must-see: https://youtube.com/@codingisfun!",
            "Hey there! Any questions? My channel 'CodingIsFun' rocks: https://youtube.com/@codingisfun!",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)




with st.columns(3)[1]:
    # st.header("hello world")
    # st.image("https://picsum.photos/200/200")
    st.image("assets/logo.png", width=225)
    st.title("CHATBOT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# File uploader for user logs
# st.sidebar.header("Upload System Logs")
# uploaded_file = st.sidebar.file_uploader("Upload your log file (CSV or JSON)", type=["csv", "json"])

user_logs = None  # Placeholder for user logs

# # Process uploaded logs
# if uploaded_file is not None:
#     file_type = uploaded_file.name.split(".")[-1]
#     if file_type == "csv":
#         user_logs = pd.read_csv(uploaded_file)
#     elif file_type == "json":
#         user_logs = pd.read_json(uploaded_file)

#     st.sidebar.success("Log file uploaded successfully!")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Accept user input
prompt = st.chat_input("What is up?")
st.write("\n")
# File uploader for user logs
uploaded_file = st.file_uploader("Upload your log file (CSV or JSON)", type=["csv", "json"])

# Process uploaded logs
if prompt or uploaded_file is not None:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(query.ask_openai(st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
