import pygame
from components import Components
class Alert():
    def __init__(self, screen):
        self.screen = screen
        self.width = 460
        self.height = 200
        self.x = self.screen.get_rect().centerx - (self.width/2)
        self.y = self.screen.get_rect().centery - (self.height/2)
        self.components = Components(self.screen)
    
    def draw(self, title, text, btn_text, status):
        if status == 1:
            alert_rect = pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 0, 19)
            title_render = self.components.getText(title, 32, True, self.components.WHITE, None, "Consolas")
            text_render = self.components.getText(text, 22, False, self.components.WHITE, None, "Consolas")
            self.screen.blit(title_render, (alert_rect.centerx - (title_render.get_width()/2), alert_rect.centery - (alert_rect.height/2) + 30))
            self.screen.blit(text_render, (alert_rect.centerx - (text_render.get_width()/2), alert_rect.centery))
            self.components.drawButton(btn_text, self.components.WHITE, alert_rect.centerx - 166/2, alert_rect.centery - 37/2 + 65, 166, 37, 0, 14, 22, False, self.components.BLACK, "Consolas")
            button_rect = pygame.Rect(alert_rect.centerx - 166/2, alert_rect.centery - 37/2 + 65, 166, 37)
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] is True:
                return True

