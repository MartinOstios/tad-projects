import pygame

class Menu():
    def __init__(self, screen, options, color, height, font_type, font_size, text_color):
        self.screen = screen
        self.options = options
        self.color = color
        self.x = 0
        self.y = 0
        self.width = self.screen.get_width()
        self.height = height
        self.font_type = font_type
        self.font_size = font_size
        self.text_color = text_color
        self.menu_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect_options = {}
        self.test = {}
        self.selected_index = 0
    
    def draw(self):
        gap = 0
        gap_value = self.menu_rect.width / len(self.options) 
        for option in self.options.keys():
            option_rect = pygame.Rect(self.x + gap, self.y, gap_value, self.height)
            if option_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, self.getHoverColor(), option_rect)
                if pygame.mouse.get_pressed()[0] is True:
                    self.selected_index = list(self.options.keys()).index(option)
            else:
                pygame.draw.rect(self.screen, self.color, option_rect)
            if list(self.options.keys()).index(option) == self.selected_index:
                pygame.draw.rect(self.screen, self.getHoverColor(), option_rect)
            font = pygame.font.SysFont(self.font_type, self.font_size)
            render_text = font.render(option, True, self.text_color, None)
            text_rect = self.screen.blit(render_text, (self.x + gap + (gap_value/2) - render_text.get_width() / 2, self.y + self.menu_rect.centery - render_text.get_height()/2))
            self.test[render_text] = (text_rect, pygame.Rect(self.menu_rect.x + gap, self.menu_rect.y, gap_value, self.menu_rect.height), self.options[option])
            if self.options[option] is not None:
                try:
                    image = pygame.image.load(self.options[option])
                    self.screen.blit(image, (text_rect.x - image.get_width() - 10, text_rect.centery - image.get_height()/2))
                except FileNotFoundError:
                    print("Error con nombre de archivo: " + self.options[option])
            gap += gap_value

    def getSelectedOption(self):
        return self.selected_index

    def getHoverColor(self):
        return (self.color[0] - (50 if self.color[0] >= 50 else -50), self.color[1] - (50 if self.color[1] >= 50 else -50), self.color[2] - (50 if self.color[2] >= 50 else -50))