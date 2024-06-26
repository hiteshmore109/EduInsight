"""
SGPA Prediction Web Application

This Flask application provides a web interface for predicting 
Semester 4 (Sem4) SGPA for individual and class data.
"""

import io
import pickle
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd
import logging

from src.DataCleaning import clean_data
from src.FeatureExtraction import get_combined_sgpa, get_sgpa

with open("models/sem5_model.pkl", "rb") as model_file:
    sem5_model = pickle.load(model_file)

with open("models/sem4_model.pkl", "rb") as model_file:
    sem4_model = pickle.load(model_file)

with open("models/sem3_model.pkl", "rb") as model_file:
    sem3_model = pickle.load(model_file)

with open("models/sem2_model.pkl", "rb") as model_file:
    sem2_model = pickle.load(model_file)

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs.log"),
    ],
)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    """Render the home page."""
    app.logger.info("Home page: Accessed Successfully")
    return render_template("index.html")


@app.route("/individual-prediction", methods=["GET", "POST"])
def individual_prediction():
    """Endpoint for individual SGPA prediction."""
    if request.method == "GET":
        app.logger.info("Individual Prediction: Accessed Successfully")
        return render_template("individual-prediction.html")
    # sem1 = request.form["sem1"]
    # sem2 = request.form["sem2"]
    # sem3 = request.form["sem3"]

    # new_data = {"Sem1": [sem1], "Sem2": [sem2], "Sem3": [sem3]}
    # df = pd.DataFrame(new_data)

    # predict = np.round(sem4_model.predict(df), decimals=1)

    # return jsonify({"prediction": predict[0]})
    # Get the form data from the request
    form_data = request.form.to_dict()
    app.logger.info(
        f"Individual Prediction: Selected number of semsters: {len(form_data)}"
    )

    # Extract the semester data from the form data
    sem_data = [value for value in form_data.values() if value]
    # for value in form_data.values():
    #     if value:
    #         sem_data.append(value)
    app.logger.info(
        f"Individual Prediction: Successfully received the following marks: {sem_data}"
    )

    # Create a dictionary with the semester data
    new_data = {f"Sem{i+1}": [sem_data[i]] for i in range(len(sem_data))}

    # Create a DataFrame with the semester data
    df = pd.DataFrame(new_data)

    num_semesters = len(sem_data)
    if num_semesters == 1:
        model = sem2_model
    elif num_semesters == 2:
        model = sem3_model
    elif num_semesters == 3:
        model = sem4_model
    else:
        model = sem5_model

    try:
        # Make the prediction
        predict = np.round(model.predict(df), decimals=1)

        return jsonify({"prediction": predict[0]})
    except Exception as e:
        app.logger.error(f"Individual Prediciton: Error occured \n\t{str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/class-prediction", methods=["GET", "POST"])
def class_prediction():
    """Endpoint for class SGPA prediction."""
    if request.method == "GET":
        app.logger.info("Class Prediction: Page accessed successfully")
        return render_template("class-prediction.html")
    # sem1 = request.files["sem1"]
    # sem2 = request.files["sem2"]
    # sem3 = request.files["sem3"]

    # sem1_cleaned = clean_data(sem1)
    # sem2_cleaned = clean_data(sem2)
    # sem3_cleaned = clean_data(sem3)

    # sem1_sgpa = get_sgpa(sem1_cleaned)
    # sem2_sgpa = get_sgpa(sem2_cleaned)
    # sem3_sgpa = get_sgpa(sem3_cleaned)

    # result = get_combined_sgpa(sem1_sgpa, sem2_sgpa, sem3_sgpa)

    # Get the form data from the request
    files = request.files.to_dict()

    try:
        # Check that each file is of type CSV
        for file in files.values():
            if not file or not file.filename.endswith(".csv"):
                return (
                    jsonify(
                        {"error": "Invalid file type. Only CSV files are allowed."}
                    ),
                    400,
                )
        # Extract the semester data from the form data
        sem_data = [clean_data(file) for file in files.values() if file]
        # for file in files.values():
        #     if file:
        #         sem_data.append(clean_data(file))
        app.logger.info(
            f"Class Prediction: Recevied files for {len(sem_data)} semesters"
        )

        # Create a list of DataFrames with the semester data
        sem_sgpa = [get_sgpa(df) for df in sem_data]

        # Determine the appropriate model based on the number of semesters
        num_semesters = len(sem_sgpa)
        if num_semesters == 1:
            model = sem2_model
        elif num_semesters == 2:
            model = sem3_model
        elif num_semesters == 3:
            model = sem4_model
        else:
            model = sem5_model

        # Combine the semester data
        result = get_combined_sgpa(*sem_sgpa)

        predict = list(np.round(model.predict(result.iloc[:, 1:]), decimals=1))
        predict = [0 if x < 4 else x for x in predict]
        result[f"Sem{num_semesters+1}_Predicted"] = predict

        # return jsonify(result.to_dict(orient='records'))
        result_csv = result.to_csv(index=False)  # Convert DataFrame to CSV string

        # Create an in-memory file-like object
        csv_file = io.BytesIO(result_csv.encode())

        # Send the file for download
        return send_file(
            csv_file,
            mimetype="text/csv",
            as_attachment=True,
            download_name="predicted_data.csv",
            conditional=True,
        )

    except Exception as e:
        app.logger.error(f"Class predicition: Error Occured \n\t {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.logger.info("Starting the Flask application....")
    app.run(host="0.0.0.0", port=5000, debug=False)
