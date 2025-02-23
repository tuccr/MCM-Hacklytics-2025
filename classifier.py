# V2 - Latest version
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def add_predictions_to_csv(model_filename, df, output_filename):

    # Step 1: Preprocess categorical columns
    df['encryption_used'] = df['encryption_used'].astype('category').cat.codes
    df['browser_type'] = df['browser_type'].astype('category').cat.codes
    df['protocol_type'] = df['protocol_type'].astype('category').cat.codes
    
    # Optionally print data types for debugging
    print(df.dtypes)

    # Step 2: Load the trained Random Forest model
    model = joblib.load(model_filename)

    # Step 3: Select features (excluding the column to exclude and session_id)
    X = df.drop(columns=['session_id'], errors="ignore")

    # Step 4: Run predictions
    df["attack_detected"] = model.predict(X)

    # Step 5: Save the updated DataFrame to a CSV file
    df.to_csv(output_filename, index=False)
    
    print(f"Predictions added and saved to {output_filename}")

    return df

