#MAIN GUI EST A APPELLE DEPUIS MAIN.PY

import pygame
from button_pygame import Button

#----CONSTANTS
BACKGROUND_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.is_clicked():
                print("Execution fonction 3x3")
            elif button_rect2.is_clicked():
                print("Execution fonction 4x4")
        
        elif False:
            pass

    # Draw the button
    button_rect.draw(screen)
    button_rect2.draw(screen)
    
    pygame.display.update()


    # Define button 
# button_rect = pygame.Rect(150, 100, 100, 50)  # x, y, width, height
# font = pygame.font.Font(None, 36)
# text_surface = font.render("3", True, WHITE)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if button_rect.collidepoint(pygame.mouse.get_pos()):
#                 print("3")

#     # Draw the button
#     screen.fill((0, 0, 0))  # Black background
#     color = LIGHT_BLUE if button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE
#     pygame.draw.rect(screen, color, button_rect)
#     screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))

#     pygame.display.update()

pygame.quit()
