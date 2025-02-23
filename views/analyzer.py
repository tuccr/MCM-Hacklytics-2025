import streamlit as st
import pandas as pd
import joblib
import classifier

# Page setup
st.title("Intrusion Detection")

# Sidebar setup
st.sidebar.title("Settings")
model_filename = '../MCM_IntrudeRF.pkl'

# Main content
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
            classifier.add_predictions_to_csv(model_filename, st.session_state.uploaded_file, output_filename)
            output_df = pd.read_csv(output_filename)
            st.session_state.output_df = output_df
            st.session_state.predictions_added = True
            st.write("Predictions added successfully!")
        except Exception as e:
            st.error(f"Error adding predictions: {e}")

    if st.session_state.predictions_added:
        csv = st.session_state.output_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download updated CSV",
            data=csv,
            file_name='intrusion_data_with_predictions.csv',
            mime='text/csv'
        )

# Reset the page
if st.button("Reset"):
    st.session_state.uploaded_file = None
    st.session_state.predictions_added = False
    st.experimental_rerun()
