import pygame
from solitaire.card import Card
pygame.init()


class Stack():
    def __init__(self, screen, quantity, x, y):
        self.screen = screen
        self.quantity = quantity
        self.x = x
        self.y = y
        self.cards = []
        self.gap_value = 18
        self.width = 122
        self.card_height = 161
        self.height = self.card_height + ((self.quantity - 1) * self.gap_value)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False
        self.add_cards()

    def add_cards(self):
        gap = 0
        for i in range(self.quantity):
            new_card = Card(self.screen, self.x, self.y + gap, self.width, self.card_height, self.gap_value, False)
            if i == self.quantity - 1:
                new_card.set_face(True)
            self.cards.append(new_card)
            gap += self.gap_value

    def draw(self):
        for card in self.cards:
            card.draw(self.clicked)
    
    def set_clicked(self, clicked):
        self.clicked = clicked
            
    def stack_pressed(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
