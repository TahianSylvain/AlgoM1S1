import itertools
import numpy as np

# Vérifie si un joueur a gagné
def check_win(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8], # lignes
        [0,3,6], [1,4,7], [2,5,8], # colonnes
        [0,4,8], [2,4,6]           # diagonales
    ]
    return any(all(board[i] == player for i in cond) for cond in win_conditions)

# Génère toutes les positions valides
def generate_positions():
    dataset = []

    # Toutes les combinaisons possibles de remplissage (3^9)
    for cells in itertools.product([0, 1, -1], repeat=9):
        x_count = cells.count(1)
        o_count = cells.count(-1)

        # Les coups doivent alterner : soit autant de X que O, soit X en a 1 de plus
        if x_count == o_count or x_count == o_count + 1:
            # Ne pas prendre les états illogiques (où les deux gagnent, ou où O gagne alors que X a plus de pions)
            if check_win(cells, 1) and check_win(cells, -1):
                continue
            if check_win(cells, -1) and x_count > o_count:
                continue

            # Étiquette : X peut-il gagner à partir d'ici ?
            label = int(check_win(cells, 1))
            dataset.append((list(cells), label))

    return dataset

# Sauvegarde en CSV
import csv

def save_to_csv(data, filename="tic_tac_toe_dataset.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cell_0","cell_1","cell_2","cell_3","cell_4","cell_5","cell_6","cell_7","cell_8","label"])
        for row, label in data:
            writer.writerow(row + [label])

# Génération
data = generate_positions()
save_to_csv(data)

print(f"Dataset généré avec {len(data)} exemples.")

# from pprint import pprint
# pprint(data[:3])