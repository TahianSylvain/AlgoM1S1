import pygame

class TextInput:
    def __init__(self, x, y, width, height, font, text_color, bg_color, border_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.text = ""
        self.active = False  # To toggle focus on the input box

    def draw(self, screen):
        # Draw the input box background and border
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Render and draw the text
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def is_clicked(self):
        result = self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        return result

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if the input box is clicked
            print("il ses fait clicker samr")
            self.active = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"User input: {self.text}")
                self.text = ""  # Clear text on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
                print("backspace mothfucjer")
            else:
                self.text += event.unicode  # Add typed character