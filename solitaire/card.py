import pygame
from components import Components
pygame.init()


class Card():
    def __init__(self, screen, x, y, width, height, gap_value, face, head, stack_number, card_color, symbol, character):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width#122
        self.height = height#161
        self.color = (0, 0, 0)
        self.card_color = card_color
        self.symbol = symbol
        self.character = character
        self.stack_number = stack_number
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.face = face
        self.head = head
        self.gap_value = gap_value
        self.components = Components(self.screen)
        self.coords_first_click = (0, 0)
        self.clicked = False
        self.set_face(self.face)

    def draw(self, clicked):
        coords = pygame.mouse.get_pos()
        self.is_clicked(clicked, coords)
        if self.clicked:
            x_difference = self.coords_first_click[0] - coords[0]
            y_difference = self.coords_first_click[1] - coords[1] 
            pygame.draw.rect(self.screen, self.color, (self.x - x_difference, self.y - y_difference, self.width, self.height), 0, 5)
            pygame.draw.rect(self.screen, self.components.BLACK, (self.x - x_difference - 1, self.y - y_difference - 1, self.width + 2, self.height + 2), 5, 5)
            if self.face:
                self.components.drawText(str(self.character), self.components.GREEN, self.card_color, self.x - x_difference,  self.y - y_difference, "Consolas", 22, True)
                self.components.drawText(str(self.symbol), self.components.GREEN, self.card_color, self.x - x_difference,  self.y - y_difference + 25, "Consolas", 22, True)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect, 0, 5)
            pygame.draw.rect(self.screen, self.components.BLACK, (self.rect.x - 1, self.rect.y - 1, self.width + 2, self.height + 2), 5, 5)
            if self.face:
                self.components.drawText(str(self.character), self.components.GREEN, self.card_color, self.rect.x, self.rect.y, "Consolas", 22, True)
                self.components.drawText(str(self.symbol), self.components.GREEN, self.card_color, self.rect.x, self.rect.y + 25, "Consolas", 22, True)

    def is_clicked(self, clicked, coords):
        if not clicked:
            if self.head:
                if self.rect.collidepoint(coords) and pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
            else:
                new_rect = pygame.Rect(self.x, self.y, self.rect.width, self.gap_value)
                if new_rect.collidepoint(coords) and pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
            self.coords_first_click = coords
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def set_face(self, face):
        self.face = face
        if self.face:
            self.color = (20, 40, 60)
        else:
            self.color = (250, 200, 100)
    
    def set_head(self, head):
        self.head = head
    

