import pygame
from components import Components
pygame.init()
class Card:
    def __init__(self, screen, x, y, character, figure):
        self.screen = screen
        self.x = x
        self.y = y
        self.character = character
        self.value = 0
        self.figure = figure
        self.visible = True
        self.components = Components(self.screen)
        self.set_value()
    
    def draw(self):
        try:
            if self.visible:
                url = "card_imgs/" + self.figure + "s/" + self.figure.capitalize() + str(self.character.upper()) + ".png"
            else:
                url = "card_imgs/cardReverse.png"
            self.components.drawImage(url, self.x, self.y)
        except FileNotFoundError:
            print("Error con la imagen")
    
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def set_value(self):
        if self.character == 'j' or self.character == 'q' or self.character == 'k' or self.character == '10':
            self.value = 10
        elif self.character == 'a':
            self.value = 11
        else:
            self.value = int(self.character)
    
