import pygame
import random

from main__GUI import dim

pygame.init()
move, width, height = 5, 400, 400
white = (255, 255, 255)
black = (0, 0, 0)
tile_size = width // dim
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Swap Puzzle")



# Create the puzzle grid
grid = [[i + j * dim for i in range(dim)] for j in range(dim)]

for inner_list in grid:
    random.shuffle(inner_list)


def draw_grid():
    for row in range(dim):
        for col in range(dim):
            value = grid[row][col]
            color = white if value else black
            pygame.draw.rect(screen, color, (col * tile_size, row * tile_size, tile_size, tile_size))
            if value:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, black)
                text_rect = text.get_rect(center=(col * tile_size + tile_size // 2, row * tile_size + tile_size // 2))
                screen.blit(text, text_rect)


count = 0
def permute_blank(row, col):
    global count

    for i in range(dim):
        for j in range(dim):
            if grid[i][j] == 0:
                blank_row, blank_col = i, j

    if abs(row - blank_row) + abs(col - blank_col) == 1:
        count += 1
        grid[blank_row][blank_col], grid[row][col] = grid[row][col], grid[blank_row][blank_col]



def swap_fully_cells(): pass
    


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // tile_size, x // tile_size
            if grid[row][col]:
                permute_blank(row, col)
                draw_grid()
                if count // move:
                    swap_fully_cells()


while True:
    draw_grid()
    handle_input()
    pygame.display.update()
