import pygame
import sys
import random
import joblib 

import pandas as pd
from sklearn import neural_network
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle

df = pd.read_csv("data_model.csv")
df = shuffle(df, random_state=42).reset_index(drop=True)
x = df.drop("Bon_coup", axis=1) 
y = df["Bon_coup"]

model = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',            
    solver='adam',                
    alpha=0.001,                  
    max_iter=2000,
    random_state=42,
    early_stopping=True           
)

model.fit(x, y)

joblib.dump(model, "tic_tac_toe_model.pkl")
print("\n✅ Modèle IA entraîné et sauvegardé dans 'tic_tac_toe_model.pkl'")

model = joblib.load("tic_tac_toe_model.pkl")  
pygame.init()

WIDTH, HEIGHT = 300, 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe avec IA")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CROSS_COLOR = (255, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
BUTTON_COLOR = (200, 200, 200)

LINE_WIDTH = 5
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 28)

board = [[None]*3 for _ in range(3)]
player = "X"
game_over = False
game_mode = None
game_started = False

def reset_game():
    global board, player, game_over
    board = [[None]*3 for _ in range(3)]
    player = "X"
    game_over = False

def draw_grid():
    SCREEN.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(SCREEN, BLACK, (i * 100, 100), (i * 100, 400), LINE_WIDTH)
        pygame.draw.line(SCREEN, BLACK, (0, 100 + i * 100), (300, 100 + i * 100), LINE_WIDTH)

def draw_marks():
    for y in range(3):
        for x in range(3):
            if board[y][x] == "X":
                pygame.draw.line(SCREEN, CROSS_COLOR, (x * 100 + 20, y * 100 + 120), (x * 100 + 80, y * 100 + 180), 4)
                pygame.draw.line(SCREEN, CROSS_COLOR, (x * 100 + 80, y * 100 + 120), (x * 100 + 20, y * 100 + 180), 4)
            elif board[y][x] == "O":
                pygame.draw.circle(SCREEN, CIRCLE_COLOR, (x * 100 + 50, y * 100 + 150), 35, 4)

def show_message(msg, y_offset=30):
    text = FONT.render(msg, True, BLACK)
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))

def draw_buttons():
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (20, 410, 80, 30))
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (110, 410, 80, 30))
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (200, 410, 80, 30))

    SCREEN.blit(SMALL_FONT.render("Menu", True, BLACK), (35, 415))
    SCREEN.blit(SMALL_FONT.render("Rejouer", True, BLACK), (115, 415))
    SCREEN.blit(SMALL_FONT.render("Quitter", True, BLACK), (215, 415))

def check_winner():
    global game_over
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            game_over = True
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        return board[0][2]
    if all(cell is not None for row in board for cell in row):
        game_over = True
        return "Draw"
    return None

def check_victory(b, joueur):
    # Vérifie si le joueur a gagné sur ce plateau `b`
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] == joueur:
            return True
        if b[0][i] == b[1][i] == b[2][i] == joueur:
            return True
    if b[0][0] == b[1][1] == b[2][2] == joueur:
        return True
    if b[0][2] == b[1][1] == b[2][0] == joueur:
        return True
    return False

def bot_move():
    empty = [(y, x) for y in range(3) for x in range(3) if board[y][x] is None]
    if not empty:
        return

    meilleur_score = -float("inf")
    meilleur_coup = None
    # 1️⃣ Vérifie si le joueur peut gagner au prochain coup
    for y, x in empty:
        test_board = [row[:] for row in board]
        test_board[y][x] = "X"  # Simule le coup du joueur

        # Simuler le coup du bot (O)
        temp_board = [row[:] for row in board]
        temp_board[y][x] = "O"

        if check_victory(temp_board, "O"):
            print('🏆 Bot joue pour gagner immédiatement !')
            board[y][x] = "O"
            return

        if check_victory(test_board, "X"):
            
            print(f"🛡️ Bot bloque à ({y}, {x}) pour éviter une défaite.")
            board[y][x] = "O"
            return
        
        
        

        # 2️⃣ Sinon, choisir le meilleur coup via le modèle IA
    
        # Convertir le board simulé en features
        flat_board = []
        for row in temp_board:
            for cell in row:
                if cell == "X":
                    flat_board.append(1)
                elif cell == "O":
                    flat_board.append(-1)
                else:
                    flat_board.append(0)

        # Obtenir les probabilités pour chaque classe (chaque case)
        proba = model.predict_proba([flat_board])[0]
        predicted_case = model.predict([flat_board])[0]
        score = proba[predicted_case]  # confiance du modèle dans son choix

        print(f"Test move ({y}, {x}) → predicted: {predicted_case}, score: {score:.2f}")

        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = (y, x)

    if meilleur_coup:
        y, x = meilleur_coup
        board[y][x] = "O"
    else:
        print("⚠️ Aucun coup optimal trouvé. Coup aléatoire.")
        y, x = random.choice(empty)
        board[y][x] = "O"



# def bot_move():
#     empty = [(y, x) for y in range(3) for x in range(3) if board[y][x] is None]
#     if not empty:
#         return

#     meilleur_score = -float("inf")
#     meilleur_coup = None

#     for y, x in empty:
#         # Simuler le coup du bot (O)
#         temp_board = [row[:] for row in board]
#         temp_board[y][x] = "O"

#         # Convertir le board simulé en features
#         flat_board = []
#         for row in temp_board:
#             for cell in row:
#                 if cell == "X":
#                     flat_board.append(1)
#                 elif cell == "O":
#                     flat_board.append(-1)
#                 else:
#                     flat_board.append(0)

#         # Obtenir les probabilités pour chaque classe (chaque case)
#         proba = model.predict_proba([flat_board])[0]
#         predicted_case = model.predict([flat_board])[0]
#         score = proba[predicted_case]  # confiance du modèle dans son choix

#         print(f"Test move ({y}, {x}) → predicted: {predicted_case}, score: {score:.2f}")

#         if score > meilleur_score:
#             meilleur_score = score
#             meilleur_coup = (y, x)

#     if meilleur_coup:
#         y, x = meilleur_coup
#         board[y][x] = "O"
#     else:
#         print("⚠️ Aucun bon coup trouvé. Coup aléatoire.")
#         y, x = random.choice(empty)
#         board[y][x] = "O"


def draw_menu():
    SCREEN.fill(WHITE)
    title = FONT.render("Choisissez un mode :", True, BLACK)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 50))

    pygame.draw.rect(SCREEN, BUTTON_COLOR, (50, 120, 200, 50))
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (50, 200, 200, 50))

    text1 = SMALL_FONT.render("2 Joueurs", True, BLACK)
    text2 = SMALL_FONT.render("Contre le Bot", True, BLACK)
    SCREEN.blit(text1, (WIDTH//2 - text1.get_width()//2, 135))
    SCREEN.blit(text2, (WIDTH//2 - text2.get_width()//2, 215))

    pygame.display.flip()

def handle_menu_click(pos):
    global game_mode, game_started
    x, y = pos
    if 50 <= x <= 250 and 120 <= y <= 170:
        game_mode = "2p"
        game_started = True
        reset_game()
    elif 50 <= x <= 250 and 200 <= y <= 250:
        game_mode = "bot"
        game_started = True
        reset_game()

def handle_bottom_buttons(pos):
    global game_started, running
    x, y = pos
    if 20 <= x <= 100 and 410 <= y <= 440:
        game_started = False
    elif 110 <= x <= 190 and 410 <= y <= 440:
        reset_game()
    elif 200 <= x <= 280 and 410 <= y <= 440:
        running = False

# === Boucle principale ===
running = True
while running:
    if not game_started:
        draw_menu()
    else:
        draw_grid()
        draw_marks()
        winner = check_winner()
        draw_buttons()

        if game_mode == "2p" and not game_over:
            show_message(f"Tour : {player}")

        if game_over:
            if winner == "Draw":
                show_message("Match nul !")
            else:
                show_message(f"{winner} gagne !")

        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            handle_bottom_buttons(pos)
            if not game_started:
                handle_menu_click(pos)
            elif game_over:
                continue
            else:
                x, y = pos
                if 100 <= y < 400:
                    row, col = (y - 100) // 100, x // 100
                    if board[row][col] is None:
                        if game_mode == "2p":
                            board[row][col] = player
                            player = "O" if player == "X" else "X"
                        elif game_mode == "bot":
                            board[row][col] = "X"
                            if not check_winner():
                                bot_move()

pygame.quit()
sys.exit()
