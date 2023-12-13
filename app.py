from flask import Flask, render_template, request
from src.DataCleaning import clean_data
from src.FeatureExtraction import get_combined_sgpa, get_sgpa

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/individual-prediction', methods=['GET', 'POST'])
def individual_prediction():
    return render_template('individual-prediction.html')

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

    return result.to_html(classes='table table-striped', render_links=True, escape=False) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)