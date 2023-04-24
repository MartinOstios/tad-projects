import pygame
from solitaire.card import Card
from solitaire.card_pool import CardPool
pygame.init()


class Stack():
    def __init__(self, screen, quantity, x, y, stack_number, card_pool):
        self.screen = screen
        self.quantity = quantity
        self.x = x
        self.y = y
        self.cards = []
        self.gap_value = 18
        self.gap = 0
        self.width = 122
        self.card_height = 161
        self.height = self.card_height + ((self.quantity - 1) * self.gap_value)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False
        self.card_pressed = None
        self.stack_number = stack_number
        self.card_pool = card_pool
        self.add_cards()

    def add_cards(self):
        for i in range(1, self.quantity + 1):
            card_data = self.card_pool.get_random_card()
            new_card = Card(self.screen, self.x, self.y + self.gap, self.width, self.card_height, self.gap_value, False, False, self.stack_number, card_data[1], card_data[2], card_data[0])
            if i == self.quantity:
                new_card.set_face(True)
                new_card.set_head(True)
            self.cards.append(new_card)
            self.gap += self.gap_value

    def draw(self):
        if len(self.cards) != 0:
            for card in self.cards:
                card.draw(self.clicked)
                if card.clicked:
                    self.card_pressed = card
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 5, 5)

    def set_clicked(self, clicked):
        self.clicked = clicked
            
    def stack_pressed(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicked:
            return True

    def stack_released(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and self.clicked:
            return True
    
    def add_new_card(self, card):
        if card not in self.cards:
            card.x = self.x
            card.y = self.y + self.gap
            card.rect = pygame.Rect(self.x, self.y + self.gap, card.width, card.height)
            card.stack_number = self.stack_number
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height + self.gap_value)
            if len(self.cards) > 0:
                self.cards[len(self.cards) - 1].set_head(False)
            card.set_head(True)
            self.gap += self.gap_value
            self.cards.append(card)
            self.card_pressed = None
    
    def remove_card(self, card):
        if card in self.cards:
            self.cards.pop()
            if len(self.cards) > 0:
                self.cards[len(self.cards) -1].set_head(True)
                self.cards[len(self.cards) -1].set_face(True)
                self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - self.gap_value)
            else:
                self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.card_height)
            self.gap -= self.gap_value
            self.card_pressed = None