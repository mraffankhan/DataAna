import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import io

# Initialize the Flask app
app = Flask(__name__)

# --- IMPORTANT ---
# This enables Cross-Origin Resource Sharing (CORS)
# It's VITAL for allowing your Netlify frontend to call your Render backend
CORS(app)

def analyze_dataframe(df):
    """
    Performs the core analysis on the student DataFrame.
    Returns analysis results as a dictionary.
    """
    
    # --- 1. Perform Calculations ---
    
    # Check for required columns
    required_cols = ['Math', 'Science', 'English']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"File must contain 'Math', 'Science', and 'English' columns.")

    df['Total'] = df[['Math', 'Science', 'English']].sum(axis=1)
    df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1).round(2)

    # Define and apply grade function
    def assign_grade(average):
        if average >= 90: return 'A'
        elif average >= 75: return 'B'
        elif average >= 60: return 'C'
        else: return 'F'
    df['Grade'] = df['Average'].apply(assign_grade)

    # --- 2. Generate Analysis Report ---
    
    # Find toppers
    math_topper = df.loc[df['Math'].idxmax()]
    science_topper = df.loc[df['Science'].idxmax()]
    english_topper = df.loc[df['English'].idxmax()]
    overall_topper = df.loc[df['Total'].idxmax()]

    analysis_report = {
        'math_topper': f"{math_topper['Name']} ({math_topper['Math']})",
        'science_topper': f"{science_topper['Name']} ({science_topper['Science']})",
        'english_topper': f"{english_topper['Name']} ({english_topper['English']})",
        'overall_topper': f"{overall_topper['Name']} (Avg: {overall_topper['Average']})",
        'weak_students': df[df['Grade'] == 'F'][['Name', 'Average', 'Grade']].to_dict('records')
    }

    # --- 3. Prepare Chart Data ---
    
    # Bar Chart: Average Score per Student
    bar_chart_data = {
        'labels': df['Name'].tolist(),
        'scores': df['Average'].tolist()
    }
    
    # Pie Chart: Grade Distribution
    grade_counts = df['Grade'].value_counts().sort_index()
    pie_chart_data = {
        'labels': grade_counts.index.tolist(),
        'counts': grade_counts.values.tolist()
    }
    
    # --- 4. Prepare Full Dataframe (as JSON) ---
    # Convert dataframe to a list of dictionaries for easy JSON serialization
    dataframe_json = df.to_dict('records')
    
    return {
        'dataframe': dataframe_json,
        'analysis_report': analysis_report,
        'bar_chart_data': bar_chart_data,
        'pie_chart_data': pie_chart_data
    }


# --- API Endpoint ---
@app.route('/analyze', methods=['POST'])
def analyze_file():
    # 1. Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
    
    file = request.files['file']
    
    # 2. Check if the file has a name
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    try:
        # 3. Read the file into a pandas DataFrame
        filename = file.filename
        if filename.endswith('.csv'):
            # Read CSV data from the in-memory file
            df = pd.read_csv(file)
        elif filename.endswith('.xlsx'):
            # Read Excel data from the in-memory file
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Invalid file type. Please upload a .csv or .xlsx file.'}), 400

        # 4. Perform the analysis
        analysis_results = analyze_dataframe(df)
        
        # 5. Return the results as JSON
        return jsonify(analysis_results), 200

    except ValueError as ve:
        # Handle custom errors (like missing columns)
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Handle other potential errors (e.g., corrupted file)
        app.logger.error(f"Error processing file: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500

# This allows running the app locally for testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
