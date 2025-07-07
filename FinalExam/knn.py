import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Example of how you might load data (replace with your actual data loading)
url = 'https://raw.githubusercontent.com/TahianSylvain/AlgoM1S1/main/FinalExam/tic_tac_toe_dataset.csv'
df = pd.read_csv(url)

# Séparer les features (X) et la cible (y)
X = df[[f"cell_{i}" for i in range(9)]]   # colonnes : cell_0 à cell_8
y = df["label"]                           # colonne cible

# Découpage entraînement / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèle KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Prédiction
y_pred = knn.predict(X_test)

# Résultat
print("Précision du modèle KNN :", accuracy_score(y_test, y_pred))
joblib.dump(knn, "modele_knn_morpion.joblib")

# =================
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

# ==================
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

# ====================================
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
