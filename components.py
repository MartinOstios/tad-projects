import pygame
pygame.init()
class Components():
    def __init__(self, screen):
        self.screen = screen
        self.BLACK = (0, 0,   0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (134, 181, 129)
        self.RED = (255, 0,   0)
        self.BLUE = (96, 151, 240)
        self.GRAY = (170, 170, 170)
        self.LIGHT_BLUE = (161, 163, 212)
    
    def getText(self, text, size, bold, color, background_color, font_type):
        font = pygame.font.SysFont(font_type, size, bold)
        render_text = font.render(text, True, color, background_color)
        return render_text

    def drawText(self, text, color, background, pos_x, pos_y, font_type, size, bold):
        self.screen.blit(self.getText(text, size, bold, color,background, font_type), (pos_x, pos_y))

    def drawImage(self, url, pos_x, pos_y):
        image = pygame.image.load(url)
        self.screen.blit(image, (pos_x, pos_y))

    def drawButton(self, text, button_color, pos_x, pos_y, width, height, border, border_radius, text_size, text_bold, text_color, text_font):
        background_rect = pygame.Rect(pos_x, pos_y, width, height)
        if background_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.getHoverColor(button_color), background_rect, border, border_radius)
        else:
            pygame.draw.rect(self.screen, button_color, background_rect, border, border_radius)
        render_text = self.getText(text, text_size, text_bold, text_color, None, text_font)
        self.screen.blit(render_text, (background_rect.x + (background_rect.width - render_text.get_width())/2, background_rect.y + (background_rect.height - render_text.get_height())/2))

    def getHoverColor(self, background_color):
        return (background_color[0] - (50 if background_color[0] >= 50 else -50), background_color[1] - (50 if background_color[1] >= 50 else -50), background_color[2] - (50 if background_color[2] >= 50 else -50))