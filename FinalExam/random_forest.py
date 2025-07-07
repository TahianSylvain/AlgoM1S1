import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Assuming your Tic-Tac-Toe data is in a pandas DataFrame
# where the columns represent the board state (e.g., 'pos1', 'pos2', ..., 'pos9')
# and the target column is 'result' (-1 for O win, 0 for draw, 1 for X win)
# You'll need to load your data into a DataFrame. Here's a placeholder:
# For example, a row might look like:
# pos1, pos2, ..., pos9, result
# 1, 0, -1, 0, 1, 0, -1, 0, 1, 1  (X wins)
# -1, 1, 0, 0, -1, 1, 0, 0, -1, 0 (O wins or Draw)
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 (O wins or Draw)

# Example of how you might load data (replace with your actual data loading)
url = 'https://raw.githubusercontent.com/TahianSylvain/AlgoM1S1/main/FinalExam/tic_tac_toe_dataset.csv'
data = pd.read_csv(url)

X = data[[f'cell_{i}' for i in range(0, 9)]]
y = data['label']

# Initialize the Random Forest Classifier
# You can adjust the n_estimators (number of trees) and other parameters
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X, y)

print("Random Forest model trained successfully.")

# You can now use the trained model to predict outcomes of Tic-Tac-Toe games
# For example, to predict the outcome of a game with a specific board state:
new_game_state = np.array([[1, 0, -1, 0, 0, 0, 0, 0, 0]]) # Example board state
prediction = model.predict(new_game_state)
print(f"Prediction for the new game state: {prediction}")
