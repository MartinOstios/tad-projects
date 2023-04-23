import pygame
from components import Components
from solitaire.stack import Stack
pygame.init()
class SolitaireView():
    def __init__(self, screen):
        self.screen = screen
        self.components = Components(self.screen)
        self.stacks = []
        self.create_stacks()
        self.clicked = False
    
    def create_stacks(self):
        gap = 0
        for i in range(1, 8):
            new_stack = Stack(self.screen, i, 31 + gap, 181)
            self.stacks.append(new_stack)
            gap += 169

    def draw(self):
        self.drawMain()

    def drawMain(self):
        pygame.draw.rect(self.screen, self.components.BLACK, (0, 50, self.screen.get_width(), self.screen.get_height() - 50), 8)
        self.components.drawText("Solitaire", self.components.BLACK, None, 545, 70, "Consolas", 22, True)
        for stack in self.stacks:
            stack.draw()
            if stack.stack_pressed():
                self.clicked = True
            stack.set_clicked(self.clicked)
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        

    def clickOnStack(self):
        for i in range(len(self.stacks)):
            pass