import pygame, webbrowser
from components import Components
pygame.init()
class Footer():
    def __init__(self, screen):
        self.screen = screen
        self.components = Components(self.screen)
        self.git_button_clicked = False
    
    def draw(self):
        git_icon = "imgs/logo-github.png"
        uam_icon = "imgs/logo-universidad.png"
        pygame.draw.rect(self.screen, self.components.BLACK, (0, 613, self.screen.get_width(), 87))
        self.components.drawText("Desarrollado por:", self.components.WHITE, None, 419, 633, "Arial", 20, True)
        self.components.drawText("Martin Ostios Arias", self.components.WHITE,None, 593, 633, "Arial", 20, False)
        self.components.drawText("@ I SEM  - 2023", self.components.WHITE,None, 512, 660, "Arial", 20, False)
        self.components.drawImage(git_icon, 787, 619)
        self.components.drawImage(uam_icon, 1037, 613)
        git_rect = pygame.Rect(787, 619, 70, 70)
        if git_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == True and not self.git_button_clicked:
                webbrowser.open(r"https://github.com/MartinOstios/tad-sll")
                self.git_button_clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.git_button_clicked = False