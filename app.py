import io
import pickle
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd

from src.DataCleaning import clean_data
from src.FeatureExtraction import get_combined_sgpa, get_sgpa

linear_model = pickle.load(open('models/model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/individual-prediction', methods=['GET', 'POST'])
def individual_prediction():
    if request.method == 'GET':
        return render_template('individual-prediction.html')
    sem1 = request.form["sem1"]
    sem2 = request.form["sem2"]
    sem3 = request.form["sem3"]

    new_data = {
    'Sem1': [sem1],
    'Sem2': [sem2],
    'Sem3': [sem3]
}
    df = pd.DataFrame(new_data)

    predict = np.round(linear_model.predict(df), decimals=1)

    return jsonify({'prediction': predict[0]})

@app.route('/class-prediction', methods=['GET', 'POST'])
def class_prediction():
    if request.method =='GET':
        return render_template('class-prediction.html')
    sem1 = request.files['sem1']
    sem2 = request.files['sem2']
    sem3 = request.files['sem3']

    sem1_cleaned = clean_data(sem1)
    sem2_cleaned = clean_data(sem2)
    sem3_cleaned = clean_data(sem3)

    sem1_sgpa = get_sgpa(sem1_cleaned)
    sem2_sgpa = get_sgpa(sem2_cleaned)
    sem3_sgpa = get_sgpa(sem3_cleaned)

    result = get_combined_sgpa(sem1_sgpa, sem2_sgpa, sem3_sgpa)

    predict = list(np.round(linear_model.predict(result.iloc[:, 1:]), decimals=1))
    predict = [0 if x < 4 else x for x in predict ]
    result['Sem4_Predicted'] = predict

    # return jsonify(result.to_dict(orient='records'))
    result_csv = result.to_csv(index=False)  # Convert DataFrame to CSV string

    # Create an in-memory file-like object
    csv_file = io.BytesIO(result_csv.encode())

    # Send the file for download
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='predicted_data.csv',
        conditional=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)