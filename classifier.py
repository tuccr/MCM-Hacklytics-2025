# V2 - Latest version
import pandas as pd
import joblib

def add_predictions_to_csv(model_filename, csv_filename, output_filename):

    # Step 1: Load the CSV data into a DataFrame
    data = pd.read_csv(csv_filename)

    # Step 2: Preprocess categorical columns
    data['encryption_used'] = data['encryption_used'].astype('category').cat.codes
    data['browser_type'] = data['browser_type'].astype('category').cat.codes
    data['protocol_type'] = data['protocol_type'].astype('category').cat.codes
    
    # Optionally print data types for debugging
    print(data.dtypes)

    # Step 3: Load the trained Random Forest model
    model = joblib.load(model_filename)

    # Step 4: Select features (excluding the column to exclude and session_id)
    X = data.drop(columns=['session_id'], errors="ignore")

    # Step 5: Run predictions
    data["Predictions"] = model.predict(X)

    # Step 6: Save the updated DataFrame to a CSV file
    data.to_csv(output_filename, index=False)
    
    print(f"Predictions added and saved to {output_filename}")

    return output_filename

