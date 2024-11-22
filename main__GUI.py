#MAIN GUI EST A APPELLE DEPUIS MAIN.PY

import pygame
from button_pygame import Button
from input_text_pygame import TextInput

#----CONSTANTS
BACKGROUND_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE = (0, 0, 255)
GRAY = (212, 207, 207)
LIGHT_BLUE = (173, 216, 230)


# Initialize Pygame
pygame.init()

# Create a display window
screen = pygame.display.set_mode((640, 500))  # Width: 400, Height: 300
pygame.display.set_caption("Pygame PUZZLE SWAP")
screen.fill(BACKGROUND_COLOR)


# dummy function to call 2ndary window
def dummy_linked_function ():
    pass

button_rect = Button(150, 100, 100, 50, dummy_linked_function, "3x3", BLUE, LIGHT_BLUE, WHITE)  # x, y, width, height

button_rect2 = Button(400, 100, 100, 50, dummy_linked_function, "4x4", BLUE, LIGHT_BLUE, WHITE)  # x, y, width, height

k_input = TextInput(200, 200, 200, 50, pygame.font.Font(None, 36), BLUE, WHITE, BLUE)

# Event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.is_clicked():
                print("Execution fonction 3x3")
                button_rect.linked_function()

            elif button_rect2.is_clicked():
                print("Execution fonction 4x4")
                button_rect2.linked_function()
        
        k_input.handle_event(event)

    # Draw the button
    button_rect.draw(screen)
    button_rect2.draw(screen)
    k_input.draw(screen)
    
    pygame.display.update()

pygame.quit()
