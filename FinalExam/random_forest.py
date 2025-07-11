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
try:
	data = pd.read_csv("./tic_tac_toe_dataset.csv")
except:
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





def get_best_predictions_for_zeros(board_state, knn_model):
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
def get_next_board():
	knn_predictions = get_knn_predictions_for_zeros(current_board_state, model)

	for board, prediction in knn_predictions:

		if prediction == 0:
			print(f"Potential board state: {board}, KNN Prediction: {prediction}")
		else:
			print(f"Potential board state: {board}, KNN Prediction: {prediction}     WIN!!!")
			return board

def find_changed_position(current_element, new_element):
  """
  Finds the position [x, y] of the element that changed between two arrays
  of the same shape.

  Args:
    current_element: A list or numpy array representing the original state.
    new_element: A list or numpy array representing the new state.

  Returns:
    A list [x, y] representing the position of the changed element, or None
    if no element changed or more than one element changed.
  """
  current_array = np.array(current_element)
  new_array = np.array(new_element)

  if current_array.shape != new_array.shape:
    return None  # Shapes must be the same

  diff = current_array != new_array
  changed_indices = np.where(diff)

  if len(changed_indices[0]) != 1:
    return None  # No element changed or more than one element changed

  x = changed_indices[0][0]
  y = changed_indices[1][0]
  return [x, y]

def convert_flat_index_to_2d(flat_index, board_shape=(3, 3)):
  """
  Converts a flat index (0-8) to a 2D board position (row, column).

  Args:
    flat_index: The flat index (an integer from 0 to 8).
    board_shape: The shape of the board (default is 3x3).

  Returns:
    A tuple (row, column) representing the 2D position.
  """
  if flat_index < 0 or flat_index >= board_shape[0] * board_shape[1]:
    return None # Index out of bounds

  row = flat_index // board_shape[1]
  col = flat_index % board_shape[1]
  return (row, col)
