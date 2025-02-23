import json
import streamlit as st
import create_data

# Initialize chat history and state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "company_info_complete" not in st.session_state:
    st.session_state.company_info_complete = False

# Main UI setup
with st.columns(3)[1]:
    st.image("assets/logo.png", width=225)
    st.title("CHATBOT")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# If company info is not yet complete
if not st.session_state.company_info_complete:
    # Display initial question if no messages exist
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("What is your company profile?")

    # Get user input
    user_input = st.chat_input("Tell me about your company")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display a processing message
        with st.chat_message("assistant"):
            st.markdown("Processing your data...please wait...")

        # Get company profile using the existing function
        company_profile = create_data.get_company_profile(user_input)

        if isinstance(company_profile, dict) and company_profile:
            # Generate files
            titles = create_data.generate_title(company_profile, 5 )
            for title in titles:
                create_data.generate_pdf(company_profile, title)
                create_data.generate_excel(company_profile, title)
                create_data.generate_text_file(company_profile, title)

            # Add success message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Thank you for providing your company information!"
            })
            st.session_state.company_info_complete = True

        # Rerun to update the UI
        st.rerun()

# Show restart button when complete
if st.session_state.company_info_complete:
    if st.button("Restart"):
        st.session_state.messages = []
        st.session_state.company_info_complete = False
        st.rerun()