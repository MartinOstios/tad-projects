
from components import Components
import pygame
pygame.init()
class Player:
    def __init__(self, screen, x, y, nickname):
        self.screen = screen
        self.x = x
        self.y = y
        self.nickname = nickname
        self.cards = []
        self.score = 0
        self.playing = False
        self.components = Components(self.screen)
    
    def add_card(self, card):
        gap = 32*len(self.cards)
        card.setX(self.x + gap)
        card.setY(self.y)
        self.cards.append(card)
        self.increase_score(card)

    
    def draw(self):
        if self.playing:
            self.components.drawText(self.nickname, self.components.RED, None, self.x + 35, self.y - 30, "Arial", 22, True)
        else:
            if self.score == 21:
                self.components.drawText(self.nickname, self.components.GREEN, None, self.x + 35, self.y - 30, "Arial", 22, False)
            else:
                self.components.drawText(self.nickname, self.components.BLACK, None, self.x + 35, self.y - 30, "Arial", 22, False)
                if self.score > 21:
                    pygame.draw.line(self.screen, self.components.BLACK, (self.x + 35, self.y - 30 + 13), (self.x + 35 + 100, self.y - 30 + 13), 3)
        self.components.drawText(str(self.score), self.components.BLACK, None, self.x + 150, self.y - 30, "Arial", 22, False)
        for card in self.cards:
            card.draw()
    
    def increase_score(self, card):
        self.score += card.get_value()
