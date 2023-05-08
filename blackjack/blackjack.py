import pygame
from components import Components
from blackjack.stack import Stack
from blackjack.crupier import Crupier
pygame.init()
class Blackjack():
    def __init__(self, screen):
        self.screen = screen
        self.components = Components(self.screen)
        self.stack = Stack(self.screen, 52)
        self.crupier = Crupier(self.screen, self.stack, 491, 119)
        self.start_rect = pygame.Rect(26, 73, 141, 37)
        self.start_pressed = False

    def draw(self):
        self.drawMain()
        self.crupier.draw()

    def drawMain(self):
        #pygame.draw.rect(self.screen, self.components.BLACK, (0, 50, self.screen.get_width(), 610), 8)
        self.components.drawImage("card_imgs/background_image.png", 0, 50)
        #self.components.drawText("Crupier", self.components.WHITE, None, 530, 78, "Arial", 22, True)
        self.components.drawButton("Doblar apuesta", self.components.BLACK, 363, 564, 141, 37, 0, 16, 16, False, self.components.WHITE, "Arial")
        self.components.drawButton("Pedir carta", self.components.BLACK, 518, 564, 141, 37, 0, 16, 16, False, self.components.WHITE, "Arial")
        self.components.drawButton("Plantarse", self.components.BLACK, 672, 564, 141, 37, 0, 16, 16, False, self.components.WHITE, "Arial")
        self.components.drawImage("card_imgs/imgBanca.png", 958, 96)
        if not self.start_pressed:
            self.components.drawButton("Empezar", self.components.BLACK, 26, 73, 141, 37, 0, 16, 16, False, self.components.WHITE, "Arial")
            self.clickOnStart()

    def clickOnStart(self):
        if self.start_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.start_pressed:
                self.start_pressed = True
                self.crupier.distribute()

