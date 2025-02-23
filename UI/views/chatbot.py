import streamlit as st

import create_data

# Initialize chat history and question index
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "current_question_asked" not in st.session_state:
    st.session_state.current_question_asked = False

# List of questions to ask
questions = [
    "What is your name?",
    "Which sector do you work in?",
    "What is your domain?",
    "What are the industry keywords?"
]

# Function to display chat messages
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Main UI setup
with st.columns(3)[1]:
    st.image("UI/assets/logo.png", width=225)
    st.title("CHATBOT")

# Display chat messages from history on app rerun
display_messages()

# Check if there are more questions to ask
if st.session_state.question_index < len(questions):
    # Get the current question
    current_question = questions[st.session_state.question_index]
    
    # Only show the input box if we haven't received an answer for the current question
    if not st.session_state.current_question_asked:
        answer = st.chat_input(current_question)
        
        if answer:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": answer})
            
            # Add assistant response to chat history
            assistant_response = f"Thank you for your answer: '{answer}'."
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Move to next question
            st.session_state.question_index += 1
            st.session_state.current_question_asked = False
            
            # Rerun the app to update the display and show the next question
            st.rerun()
    
# If all questions have been answered, show a thank you message and restart option
if st.session_state.question_index >= len(questions):
    company_profile = {
        "name": st.session_state.messages[0]["content"],
        "sector": st.session_state.messages[1]["content"],
        "domain": st.session_state.messages[2]["content"],
        "industry_keywords": st.session_state.messages[3]["content"].split(",")
    }

    titles = create_data.generate_title(company_profile, 5)
    # Generate multiple honeypot files
    for title in titles:
        create_data.generate_pdf(company_profile, title)
        create_data.generate_excel(company_profile, title)
        create_data.generate_text_file(company_profile, title)
    
    st.markdown()
    st.success("Thank you for answering all the questions!")
    if st.button("Restart"):
        st.session_state.messages = []
        st.session_state.question_index = 0
        st.session_state.current_question_asked = False
        st.rerun()