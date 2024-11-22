import pygame

class Button:
    def __init__(self, x, y, width, height, linked_function, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.linked_function = linked_function

    def draw(self, screen):
        current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self):
        result = self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        self.linked_function()
        return result