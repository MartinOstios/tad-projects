import pygame
class Alert():
    def __init__(self, screen):
        self.screen = screen
        self.width = 460
        self.height = 200
        self.x = self.screen.get_rect().centerx - (self.width/2)
        self.y = self.screen.get_rect().centery - (self.height/2)
    
    def draw(self, title, text, btn_text, status):
        if status == 1:
            alert_rect = pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 0, 19)
            self.screen.blit(title, (alert_rect.centerx - (title.get_width()/2), alert_rect.centery - (alert_rect.height/2) + 30))
            self.screen.blit(text, (alert_rect.centerx - (text.get_width()/2), alert_rect.centery))
            button_rect = pygame.draw.rect(self.screen, (255, 255, 255), (alert_rect.centerx - 166/2, alert_rect.centery - 37/2 + 65, 166, 37), 0, 14)
            self.screen.blit(btn_text, (button_rect.x + (button_rect.width - btn_text.get_width())/2, button_rect.y + (button_rect.height - btn_text.get_height())/2))
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] is True:
                return True

