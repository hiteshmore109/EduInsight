# tests/test_data_cleaning.py
from tempfile import NamedTemporaryFile
import os
import pandas as pd
from src.DataCleaning import parse_grace_condone, clean_data

def test_parse_grace_condone():
    assert parse_grace_condone("11*5") == 16
    assert parse_grace_condone("20@3") == 23
    assert parse_grace_condone(15) == 15
    assert parse_grace_condone("15") == 15

def test_clean_data():
    data = pd.DataFrame({
        'StudentId': [1, 2],
        'StudentName': ['Student1', 'Student2'],
        'BIT1': [80, 'CC'],
        'BIT2': ['AB', 75]
    })
    # data = data.to_csv()
    # cleaned_data = clean_data(data)
    with NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as temp_csv:
        data.to_csv(temp_csv, index=False)
        # Use the temporary CSV file for testing
    print(pd.read_csv(temp_csv.name))
    cleaned_data = clean_data(temp_csv.name)
    assert cleaned_data.iloc[0, 3] == 0
    assert cleaned_data.iloc[1, 2] == 0
    os.remove(temp_csv.name)