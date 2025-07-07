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
current_board_state = [[1, 0, -1, 0, 1, 0, -1, 0, 0]]
# You can now use the trained model to predict outcomes of Tic-Tac-Toe games
# For example, to predict the outcome of a game with a specific board state:
new_game_state = np.array(current_board_state) # Example board state
prediction = model.predict(new_game_state)
print(f"Prediction for the new game state: {prediction}")





import numpy as np
def get_knn_predictions_for_zeros(board_state, knn_model):
  """
  Given a board state, return a list of potential board states and their
  KNN predictions for all possible moves into empty cells (represented by 0).

  Args:
    board_state: A list or numpy array representing the current board state.
                 e.g., [[1, 0, -1, 0, 0, 0, 0, 0, 0]]
    knn_model: The trained KNeighborsClassifier model.

  Returns:
    A list of tuples, where each tuple contains:
    - A numpy array representing a potential new board state.
    - The KNN prediction for that potential board state.
  """
  predictions = []
  board_array = np.array(board_state).flatten()

  for i in range(len(board_array)):
    if board_array[i] == 0:
      # Create a potential new board state by placing '1' (assuming bot is 'X')
      new_board_array = board_array.copy()
      new_board_array[i] = 1

      # Reshape to the expected input format for the KNN model
      new_board_state = new_board_array.reshape(1, -1)

      # Get the KNN prediction for this potential state
      prediction = knn_model.predict(new_board_state)[0]

      predictions.append((new_board_state, prediction))

  return predictions
  

# Load the trained KNN model (assuming it's saved as "modele_knn_morpion.joblib")
# If the model is not already loaded in the environment, uncomment the following line
# knn = joblib.load("modele_knn_morpion.joblib")

# Example usage:
current_board_state = [[1, 0, -1, 0, 1, 0, -1, 0, 0]]
knn_predictions = get_knn_predictions_for_zeros(current_board_state, knn)

for board, prediction in knn_predictions:
  print(f"Potential board state: {board}, KNN Prediction: {prediction}") if prediction == 0 else print(f"Potential board state: {board}, KNN Prediction: {prediction}     WIN!!!")
