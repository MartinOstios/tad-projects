import pygame, time, threading
from blackjack.player import Player
from components import Components
from blackjack.stack import Stack
pygame.init()


class Crupier:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.stack = Stack(self.screen, 52)
        self.x = x
        self.y = y
        self.cards = []
        self.score = 0
        self.players = []
        self.create_players()
        self.actual_shift = -1  # 0: Crupier, 1: Jugador 1, 2: Jugador 2, 3: Jugador 3
        self.components = Components(self.screen)

        # Buttons rect
        self.ask_rect = pygame.Rect(448, 564, 141, 37)
        self.stand_rect = pygame.Rect(602, 564, 141, 37)
        self.click_on_bet = False
        self.click_on_ask = False
        self.click_on_stand = False
        self.crupier_bool = False
        self.continue_game = False
        self.actual_card = None
        self.actual_player = None

        # Threads
        self.threads = []
        self.threads_finish = []
        self.crupier_task_finished = pygame.USEREVENT
        #self.crupier_task = threading.Thread(target=self.distribute_own_cards)
        self.crupier_reset_task_finished = pygame.USEREVENT
        #self.crupier_reset_task = threading.Thread(target=self.pass_round)

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
        for player in self.players:
            player.draw()
        self.play()
        self.playShift()
        self.updatePlaying()

    def playShift(self):
        if self.actual_shift == 0:
            if not self.crupier_bool:
                self.crupier_bool = True
                self.threads.append(threading.Thread(target=self.distribute_own_cards))         
                self.threads[-1].start()
            # Mostrar ganadores
            if self.continue_game:
                self.continue_game = False
                self.game_winners()
                self.threads.append(threading.Thread(target=self.pass_round))         
                self.threads[-1].start()
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
        self.components.drawText("Crupier", self.components.BLACK, None, self.x + 65, self.y - 30, "Arial", 22, False)
        pygame.draw.rect(self.screen, self.components.BLACK, (self.x, self.y, 200, 126), 3, 1)
    
    def addCard(self, card):
        gap = 32*len(self.cards)
        card.setX(self.x + gap)
        card.setY(self.y)
        self.cards.append(card)
        if self.score + card.value > 21:
            for card in self.cards:
                if card.value == 11:
                    print("Cambiando score de A")
                    card.value = 1
        self.score = sum([card.value for card in self.cards])
    
    def distribute_own_cards(self):
        time.sleep(2)
        print("Distribuyendo cartas, score: " + str(self.score))
        self.cards[1].visible = True
        while self.score < 16:
            time.sleep(2)
            card = self.stack.remove_card()
            self.addCard(card)
        self.continue_game = True
        pygame.event.post(pygame.event.Event(self.crupier_task_finished))

    def pass_round(self):
        time.sleep(5)
        for player in self.players:
            player.cards.clear()
            player.winner = None
            player.score = 0
        self.cards.clear()
        self.score = 0
        self.stack = Stack(self.screen, 52)
        self.actual_shift = -1
        time.sleep(2)
        self.distribute()
        self.continue_game = False
        self.crupier_bool = False
        pygame.event.post(pygame.event.Event(self.crupier_reset_task_finished))

    def game_winners(self):
        for player in self.players:
            if self.score <= 21:
                if player.score <= 21:
                    if player.score == self.score:
                        print(f"El jugador {player.nickname} empató con la casa")
                        player.winner = 3
                    if player.score > self.score:
                        print(f"El jugador {player.nickname} ganó a la casa")
                        player.winner = 1
                    if player.score < self.score:
                        print(f"El jugador {player.nickname} perdió contra la casa")
                        player.winner = 2
                else:
                    print(f"El jugador {player.nickname} perdió contra la casa")
                    player.winner = 2
            else:
                if player.score <= 21:
                    print(f"El jugador {player.nickname} ganó a la casa")
                    player.winner = 1
                else:
                    print(f"El jugador {player.nickname} perdió contra la casa")
                    player.winner = 2
