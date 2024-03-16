"""
Model Training Script

This script trains a Ridge Regression model to predict Semester 4 
(Sem4) SGPA based on the SGPA data from previous semesters.
It also creates a pickle file of the trained model when run exclusively.
"""
import cloudpickle
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, GridSearchCV

from DataCleaning import clean_data
from FeatureExtraction import get_combined_sgpa, get_sgpa


def load_data() -> pd.DataFrame:
    """
    Load the necessary data required to train the model and return the
    DataFrame of the combined data with SGPA.

    Returns:
    - pd.DataFrame: A DataFrame containing combined SGPA data from multiple semesters.
    """
    sem1 = "../data/Sem1 October-21.csv"
    sem2 = "../data/Sem2 March-22.csv"
    sem3 = "../data/Sem3 October-22.csv"
    sem4 = "../data/Sem4 March-23.csv"

    sem1_cleaned = clean_data(sem1)
    sem2_cleaned = clean_data(sem2)
    sem3_cleaned = clean_data(sem3)
    sem4_cleaned = clean_data(sem4)

    sem1_sgpa = get_sgpa(sem1_cleaned)
    sem2_sgpa = get_sgpa(sem2_cleaned)
    sem3_sgpa = get_sgpa(sem3_cleaned)
    sem4_sgpa = get_sgpa(sem4_cleaned)

    result = get_combined_sgpa(sem1_sgpa, sem2_sgpa, sem3_sgpa, sem4_sgpa)
    return result


def sem4_model(result: pd.DataFrame):
    """
    Train the required model using Ridge Regression with hyperparameter tuning.

    Parameters:
    - result (pd.DataFrame): A DataFrame containing combined SGPA data from multiple semesters.

    Returns:
    - Ridge: The trained Ridge Regression model.
    """
    features = ["Sem1", "Sem2", "Sem3"]
    target = "Sem4"

    X = result[features]
    y = result[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=40
    )

    ridge_model = Ridge()

    param_grid = {"alpha": np.logspace(-6, 6, 1000)}

    grid_search = GridSearchCV(
        ridge_model, param_grid, cv=5, scoring="neg_mean_squared_error"
    )
    grid_search.fit(X_train, y_train)

    # Get the best hyperparameters
    best_alpha = grid_search.best_params_["alpha"]

    # Train the Ridge Regression model with the best hyperparameters
    best_ridge_model = Ridge(alpha=best_alpha)
    best_ridge_model.fit(X_train, y_train)

    return best_ridge_model


if __name__ == "__main__":
    # Use the model to predict SGPA for new data
    new_data = {
        "Sem1": [8.7, 9.1, 8.9, 9.9, 8.4, 8.7, 8.9],
        "Sem2": [8.6, 8.5, 9.1, 9.4, 6.9, 9.0, 9.3],
        "Sem3": [9.2, 9.1, 9.5, 9.8, 7.6, 8.9, 8.6],
    }

    new_df = pd.DataFrame(new_data)

    data = load_data()

    ridge = sem4_model(data)

    # Make predictions for the new data
    new_predictions = list(np.round(ridge.predict(new_df), decimals=1))
    new_df["Sem4_Predicted"] = new_predictions

    # Display the predictions
    print("\nPredictions for new data:")
    print(new_predictions)

    print(new_df)

    # Save the function to a pickle file
    with open("../models/sem4_model.pkl", "wb") as f:
        cloudpickle.dump(ridge, f)
