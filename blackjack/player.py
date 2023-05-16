
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
        self.money = 0
        self.score = 0
        self.playing = False
        self.winner = None
        self.player_rect = pygame.Rect(self.x, self.y, 200, 126)
        self.components = Components(self.screen)
    
    def add_card(self, card):
        gap = 32*len(self.cards)
        card.setX(self.x + gap)
        card.setY(self.y)
        self.cards.append(card)
        if self.score + card.value > 21:
            for card in self.cards:
                if card.value == 11:
                    card.value = 1
        self.increase_score()
        

    
    def draw(self):
        for card in self.cards:
            card.draw()
        pygame.draw.rect(self.screen, self.components.BLACK, self.player_rect, 3, 1)
        if self.playing:
            text_render = self.components.getText(self.nickname, 22, True, self.components.RED, None, "Arial")
            self.screen.blit(text_render, (self.player_rect.centerx - (text_render.get_width() / 2), self.player_rect.y - 30))
        else:
            if self.score == 21:
                text_render = self.components.getText(self.nickname, 22, True, self.components.GREEN, None, "Arial")
                self.screen.blit(text_render, (self.player_rect.centerx - (text_render.get_width() / 2), self.player_rect.y - 30))
            else:
                text_render = self.components.getText(self.nickname, 22, True, self.components.BLACK, None, "Arial")
                self.screen.blit(text_render, (self.player_rect.centerx - (text_render.get_width() / 2), self.player_rect.y - 30))
                if self.score > 21:
                    pygame.draw.line(self.screen, self.components.RED, 
                        (self.player_rect.centerx - (text_render.get_width() / 2),
                        self.player_rect.y - 30 + (text_render.get_height() / 2)),
                        (self.player_rect.centerx + (text_render.get_width() / 2),
                        self.player_rect.y - 30 + (text_render.get_height() / 2)), 2)
        self.draw_score()
        if self.winner != None:
            if self.winner == 1:
                self.draw_result_message("¡Ganaste!")
            elif self.winner == 2:
                self.draw_result_message("Perdiste")
            elif self.winner == 3:
                self.draw_result_message("Empate")
    
    def increase_score(self):
        self.score = sum([card.value for card in self.cards])

    def draw_result_message(self, message):
        text_render = self.components.getText(message, 22, False, self.components.WHITE, None, "Arial")
        x = self.player_rect.centerx - (text_render.get_width() / 2) - 10
        y = self.player_rect.centery - (text_render.get_height() / 2) - 5
        width = text_render.get_width() + 20
        height = text_render.get_height() + 10
        alert_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.components.BLACK, alert_rect, 0, 5)
        self.screen.blit(text_render, (self.player_rect.centerx - (text_render.get_width() / 2), self.player_rect.centery - (text_render.get_height() / 2)))

    def draw_score(self):
        text_render = self.components.getText(str(self.score), 40, False, self.components.WHITE, None, "Arial")
        x = self.player_rect.midbottom[0] - (text_render.get_width() / 2) - 10
        y = self.player_rect.midbottom[1] + 30 - (text_render.get_height() / 2) - 5
        width = text_render.get_width() + 20
        height = text_render.get_height() + 10
        alert_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.components.BLACK, alert_rect, 0, 5)
        self.screen.blit(text_render, (self.player_rect.midbottom[0] - (text_render.get_width() / 2), self.player_rect.midbottom[1] + 30 - (text_render.get_height() / 2)))

