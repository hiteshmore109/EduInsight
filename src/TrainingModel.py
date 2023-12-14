import cloudpickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from DataCleaning import clean_data
from FeatureExtraction import get_combined_sgpa, get_sgpa

sem1 = '../data/FY- Sem I 2021-22 Marksheet.csv'
sem2 = '../data/FY- Sem II 2021-22 Marksheet.csv'
sem3 = '../data/SY- Sem III 2022-23October 2022 Marksheet.csv'
sem4 = '../data/SY- Sem IV 2022-23October 2022 Marksheet.csv'

sem1_cleaned = clean_data(sem1)
sem2_cleaned = clean_data(sem2)
sem3_cleaned = clean_data(sem3)
sem4_cleaned = clean_data(sem4)

sem1_sgpa = get_sgpa(sem1_cleaned)
sem2_sgpa = get_sgpa(sem2_cleaned)
sem3_sgpa = get_sgpa(sem3_cleaned)
sem4_sgpa = get_sgpa(sem4_cleaned)

result = get_combined_sgpa(sem1_sgpa, sem2_sgpa, sem3_sgpa, sem4_sgpa)

features = ['Sem1', 'Sem2', 'Sem3']
target = 'Sem4'

X = result[features]
y = result[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = linear_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Use the model to predict SGPA for new data
new_data = {
    'Sem1': [8.7, 9.1, 8.9, 9.9, 8.4, 8.7, 8.9],
    'Sem2': [8.6, 8.5, 9.1, 9.4, 6.9, 9.0, 9.3],
    'Sem3': [9.2, 9.1, 9.5, 9.8, 7.6, 8.9, 8.6]
}

new_df = pd.DataFrame(new_data)

# Make predictions for the new data
new_predictions = list(np.round(linear_model.predict(new_df), decimals=1))
new_df['Sem4_Predicted'] = new_predictions

# Display the predictions
print('\nPredictions for new data:')
print(new_predictions)

print(new_df)

# Save the function to a pickle file
with open("../models/model.pkl", 'wb') as f:
    cloudpickle.dump(linear_model, f)