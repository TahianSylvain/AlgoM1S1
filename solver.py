import random as rd
import math
import heapq
import numpy as np

# État final
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
goal_position = {value: (i, j) for i, row in enumerate(goal_state) for j, value in enumerate(row)}

# Fonction heuristique : Distance de Manhattan
def heuristic(state):
    distance = 0
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value != 0:  # Ignore la case vide
                goal_i, goal_j = goal_position[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

# Trouve la position de la case vide (0)
def find_zero(state):
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return i, j

# Génère les nouveaux états possibles
def get_neighbors(state):
    i, j = find_zero(state)
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:  # Vérifie les limites
            new_state = [row[:] for row in state]  # Copie du tableau
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]  # Échange
            neighbors.append(new_state)
    return neighbors

# A* Algorithm
def a_star(initial_state):
    priority_queue = []
    heapq.heappush(priority_queue, (0, initial_state, 0, []))  # (f(n), état, g(n), chemin)
    visited = set()

    while priority_queue:
        f, current_state, g, path = heapq.heappop(priority_queue)
        current_tuple = tuple(tuple(row) for row in current_state)

        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        # Vérifie si l'objectif est atteint
        if current_state == goal_state:
            return path + [current_state]

        # Explore les voisins
        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                h = heuristic(neighbor)
                heapq.heappush(priority_queue, (g + 1 + h, neighbor, g + 1, path + [current_state]))

    return None  # Aucun chemin trouvé




def main():
    n = 8
    dim = int(math.sqrt(n+1))
    k = 0
    
    initial_state = [[1, 2, 3], [0, 4, 6], [7, 5, 8]]
    solution = a_star(initial_state)

    if solution:
        for step in solution:
            print(np.array(step))
            print()
    

if __name__ == "__main__":
    main()