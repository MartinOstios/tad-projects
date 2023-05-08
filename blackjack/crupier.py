import pygame, time
from blackjack.player import Player
from components import Components
pygame.init()


class Crupier:
    def __init__(self, screen, stack, x, y):
        self.screen = screen
        self.stack = stack
        self.x = x
        self.y = y
        self.cards = []
        self.score = 0
        self.players = []
        self.create_players()
        self.actual_shift = -1  # 0: Crupier, 1: Jugador 1, 2: Jugador 2, 3: Jugador 3
        self.components = Components(self.screen)

        # Buttons rect
        self.double_bet_rect = pygame.Rect(363, 564, 141, 37)
        self.ask_rect = pygame.Rect(518, 564, 141, 37)
        self.stand_rect = pygame.Rect(672, 564, 141, 37)
        self.click_on_bet = False
        self.click_on_ask = False
        self.click_on_stand = False

    def create_players(self):
        player1 = Player(self.screen, 816, 300, "Jugador 1")
        player2 = Player(self.screen, 494, 376, "Jugador 2")
        player3 = Player(self.screen, 136, 300, "Jugador 3")
        self.players.extend([player1, player2, player3])

    def distribute(self):
        print("DISTRIBUIR")
        for i in range(2):
            for player in self.players:
                card = self.stack.remove_card()
                player.add_card(card)
        # Crupier cards
        card1 = self.stack.remove_card()
        card2 = self.stack.remove_card()
        card2.visible = False
        self.addCard(card1)
        self.addCard(card2)
        self.actual_shift += 2

    def draw(self):
        self.components.drawText("Shift: " + str(self.actual_shift), self.components.BLACK, None, 26, 120, "Arial", 22, True)
        for player in self.players:
            player.draw()
        self.play()
        self.playShift()
        self.updatePlaying()

    def playShift(self):
        if self.actual_shift == 0:
            self.cards[1].visible = True
            while self.score < 16:
                pygame.time.wait(100)
                card = self.stack.remove_card()
                self.addCard(card)
            
        if self.actual_shift > 0:
            player = self.players[self.actual_shift - 1]
            if player.score != 21:
                if self.ask_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.click_on_ask:
                    self.click_on_ask = True
                    card = self.stack.remove_card()
                    player.add_card(card)
                    if player.score > 21:
                        self.actual_shift += 1
            if self.stand_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.click_on_stand:
                    self.click_on_stand = True
                    self.actual_shift += 1

        if not pygame.mouse.get_pressed()[0]:
            self.click_on_ask = False
            self.click_on_bet = False
            self.click_on_stand = False

        if self.actual_shift == 4:
            self.actual_shift = 0
    
    def updatePlaying(self):
        for player in self.players:
            player.playing = False
        if self.actual_shift != 0 and self.actual_shift != -1:
            self.players[self.actual_shift - 1].playing = True
    
    def play(self):
        for card in self.cards:
            card.draw()
    
    def addCard(self, card):
        gap = 32*len(self.cards)
        card.setX(self.x + gap)
        card.setY(self.y)
        self.cards.append(card)
        self.score += card.get_value()
