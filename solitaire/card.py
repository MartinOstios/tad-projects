import pygame
from components import Components
pygame.init()


class Card():
    def __init__(self, screen, x, y, width, height, gap_value, face):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width#122
        self.height = height#161
        self.color = (0, 0, 0)
        self.number = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.face = face
        self.gap_value = gap_value
        self.components = Components(self.screen)
        self.clicked = False
        self.x_difference = 0
        self.set_face(self.face)

    def draw(self, clicked):
        coords = pygame.mouse.get_pos()
        self.is_clicked(clicked, coords)
        if self.clicked:
            pygame.draw.rect(self.screen, self.color, (coords[0], coords[1], self.width, self.height), 0, 5)
            pygame.draw.rect(self.screen, self.components.BLACK, (coords[0] - 1, coords[1] - 1, self.width + 2, self.height + 2), 5, 5)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect, 0, 5)
            pygame.draw.rect(self.screen, self.components.BLACK, (self.rect.x - 1, self.rect.y - 1, self.width + 2, self.height + 2), 5, 5)

    def is_clicked(self, clicked, coords):
        if not clicked:
            if self.face:
                if self.rect.collidepoint(coords) and pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
            if not self.face:
                new_rect = pygame.Rect(self.x, self.y, self.width, self.gap_value)
                if new_rect.collidepoint(coords) and pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def set_face(self, face):
        self.face = face
        if self.face:
            self.color = (20, 40, 60)
        else:
            self.color = (250, 200, 100)

