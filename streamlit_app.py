import streamlit as st


# --- PAGE SETUP ---
project_2_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
    default=True
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Projects": [project_2_page],
    }
)


# --- SHARED ON ALL PAGES ---
# with st.sidebar:
#   st.image("assets/logo.png", width=150)
st.logo("assets/logo.png", size="large")
#st.sidebar.markdown("Made with ❤️ by [Sven](https://youtube.com/@codingisfun)")


# --- RUN NAVIGATION ---
pg.run()
