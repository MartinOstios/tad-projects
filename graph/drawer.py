import pygame
from components import Components
import random
class Drawer:
    def __init__(self, screen, x, y, width, height, users):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.users = users
        self.graph_type = "friends"
        self.node_positions = {}
        self.components = Components(self.screen)
        self.set_positions()

    def draw(self):
        self.draw_connections()
        self.draw_nodes()
        

    def draw_connections(self):
        for user in self.users:
            start_pos = self.node_positions.get(user["id"])  # Verificar si la clave existe en node_positions
            if start_pos is not None and self.graph_type in user:
                for connection in user[self.graph_type]:
                    end_pos = self.node_positions.get(connection["id"])  # Verificar si la clave existe en node_positions
                    if end_pos is not None:
                        pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)

    def draw_nodes(self):
        for user in self.users:
            pos = self.node_positions.get(user["id"])  # Verificar si la clave existe en node_positions
            if pos is not None:
                x, y = pos
                profile_image = user.get("profile_image")
                if profile_image is not None:
                    image_width, image_height = profile_image.get_size()
                    image_x = x - image_width // 2
                    image_y = y - image_height // 2
                    text_render = self.components.getText(user["name"], 15, False, self.components.WHITE, None, "Arial")
                    name_rect = pygame.Rect(image_x + image_width // 2 - (text_render.get_width()/2) - 5, image_y + image_height // 2 + 25, text_render.get_width() + 10, text_render.get_height() + 5)
                    self.screen.blit(profile_image, (image_x, image_y))
                pygame.draw.rect(self.screen, self.components.BLACK, name_rect, 0, 5)
                self.screen.blit(text_render, (name_rect.x + (name_rect.width - text_render.get_width())/2, name_rect.y + (name_rect.height - text_render.get_height())/2))
    
    def set_positions(self):
        # Calcular las coordenadas de los nodos
        x_spacing = self.width // (len(self.users) + 1)
        y_spacing = self.height // (len(self.users) + 1)
        y_positions = [random.randint(y_spacing, self.height - y_spacing) for _ in range(len(self.users))]
        for i, user in enumerate(self.users):
            x = (i + 1) * x_spacing
            y = y_positions[i]
            self.node_positions[user["id"]] = (x, y)
    

    def set_data(self, users, graph_type):
        self.users = users
        #graph_type = friends, family
        self.graph_type = graph_type
        self.set_positions()
    
        
    
