from single_linked_list import *
import pygame
import sys
from footer import Footer
from menu import Menu
from components import Components
from sll_view import SLLView
from solitaire.solitaire_view import SolitaireView
from blackjack.blackjack import Blackjack
pygame.init()
class Superheroes:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("TAD")
        self.components = Components(self.screen)
        self.footer = Footer(self.screen)
        self.menu = Menu(self.screen, {"SLL": "imgs/list-outline.png", "Pilas": "imgs/list-outline.png", "Solitaire": "imgs/list-outline.png", "Grafos": "imgs/circle-nodes-solid.png"}, self.components.GREEN, 50, "Consolas", 22, self.components.WHITE)
        self.sll_view = SLLView(self.screen)
        self.solitaire_view = SolitaireView(self.screen)
        self.blackjack_view = Blackjack(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.components.WHITE)
            if(self.menu.getSelectedOption() == 0):
                self.sll_view.draw()
            if(self.menu.getSelectedOption() == 1):
                self.blackjack_view.draw()
            if(self.menu.getSelectedOption() == 2):
                self.solitaire_view.draw()
            self.menu.draw()
            self.footer.draw()
            pygame.display.flip()


if __name__ == "__main__":
    a = Superheroes()
    a.run()
