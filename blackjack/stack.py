import pygame
pygame.init()
from blackjack.card import Card
from blackjack.card_pool import CardPool
class Stack():
    def __init__(self, screen, quantity):
        self.screen = screen
        self.quantity = quantity
        self.cards = []
        self.card_pool = CardPool()
        self.fill_stack()
    
    def fill_stack(self):
        for i in range(self.quantity):
            card_values = self.card_pool.get_random_card()
            self.cards.append(Card(self.screen, 958, 96, card_values[0], card_values[2]))
    
    def remove_card(self):
        return self.cards.pop()