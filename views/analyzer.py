import shutil
import streamlit as st
import pandas as pd
import classifier
import os

# Page setup
st.title("Intrusion Detection")

def clear_file(file_path):
    if os.path.exists(file_path):
        print(f"Clearing file: {file_path}")
        # Open the file in write mode to clear its content
        with open(file_path, "w") as file:
            file.truncate(0)  # Clear the file content

# Sidebar setup
#st.sidebar.title("Settings")
model_filename = 'best_intrusion_rf.pkl'

# Main content
st.markdown("""
This application is designed to detect intrusions in network traffic data.
The data is meant to resemble [this cyber intrusion detection dataset on Kaggle](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset/data).
""")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'predictions_added' not in st.session_state:
    st.session_state.predictions_added = False

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    st.session_state.predictions_added = False
    st.write("CSV file uploaded successfully!")

if st.session_state.uploaded_file is not None:
    if st.button("Make Predictions"):
        try:
            df = pd.read_csv(st.session_state.uploaded_file)
            output_filename = 'intrusion_data_with_predictions.csv'
            if df.empty:
                st.error("Uploaded CSV file is empty.")
            else:
                st.write("Data before adding predictions:")
                st.write(df.head())
                
                output_df = classifier.add_predictions_to_csv(model_filename, df, output_filename)
                
                # Check if the file was written correctly
                # with open(output_filename, 'r') as f:
                #     content = f.read()
                #     st.write("Content of the output file:")
                #     st.text(content)
                
                output_df = pd.read_csv(output_filename)
                st.session_state.output_df = output_df
                st.session_state.predictions_added = True
                st.write("Predictions added successfully!")
                st.write("Data after adding predictions:")
                st.write(output_df.head())
        except Exception as e:
            st.error(f"Error adding predictions: {e}")

 
    if st.session_state.predictions_added:
        csv = st.session_state.output_df.to_csv(index=False).encode('utf-8')
        if st.download_button(
            label="Download updated CSV",
            data=csv,
            file_name='intrusion_data_with_predictions.csv',
            mime='text/csv'
        ):
            try:
                clear_file('MCM-HACKALYTICS-2025/intrusion_data_with_predictions.csv')
                #os.remove('MCM-HACKALYTICS-2025/intrusion_data_with_predictions.csv')
                st.success("File downloaded and deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting file: {e}")

