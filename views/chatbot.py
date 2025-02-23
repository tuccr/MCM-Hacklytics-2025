import streamlit as st
import json
import os
import shutil
import zipfile
from create_data import get_company_profile, generate_title, generate_pdf, generate_excel, generate_text_file

def clear_honeypot_directory():
    if os.path.exists("honeypot_files"):
        shutil.rmtree("honeypot_files")
    os.makedirs("honeypot_files", exist_ok=True)

def zip_files(output_dir):
    zip_filename = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_dir))
    return zip_filename

# Streamlit UI
st.image("assets/logo.png")
with st.columns([2, 8, 1])[1]:
    st.title("Honeypot File Generator")
st.write("Enter your company profile details:")
user_input = st.text_area("Company Profile (JSON or descriptive text)")

if st.button("Turn in Company Profile"):
    company_profile = get_company_profile(user_input)
    if not company_profile:
        st.error("I'm sorry, but I need more information to gather details about your company. Kindly furnish the following information: Company Name, Sector, Domain, and Industry Keywords")
    else:
        st.session_state.company_profile = company_profile
        st.success("Company profile successfully parsed!")

if "company_profile" in st.session_state:
    num_files = st.number_input("Enter the number of sets of honeypot files to generate:", min_value=1, max_value=50, step=1)
    if st.button("Generate Files"):
        clear_honeypot_directory()
        titles = generate_title(st.session_state.company_profile, num_files)
        if (len(titles)>num_files):
            titles = titles[:num_files]
            print(len(titles))
        for title in titles:
            generate_pdf(st.session_state.company_profile, title)
            generate_excel(st.session_state.company_profile, title)
            generate_text_file(st.session_state.company_profile, title)
        
        zip_path = zip_files("honeypot_files")
        
        with open(zip_path, "rb") as f:
            st.download_button("Download Honeypot Files", f, file_name="honeypot_files.zip", mime="application/zip")
        
        clear_honeypot_directory()
        os.remove(zip_path)
