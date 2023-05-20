from components import Components
import pygame
from combo_box import ComboBox
class SideMenu:
    def __init__(self, screen, x, y, width, height, color, users, relationships):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.users = users
        self.relationships = relationships
        self.user_names = [str(user["name"]) for user in self.users]
        self.color = color
        self.components = Components(self.screen)
        self.rect_button_accept_upper = pygame.Rect(1248, 235, 103, 30)
        self.rect_button_accept_upper_clicked = False
        self.rect_upper = pygame.Rect(x, y, self.width, self.height/2)
        self.rect_lower = pygame.Rect(x, y + self.height/2, self.width, self.height/2)
        self.rect_combo_user_upper = pygame.Rect(1211, 38, 177, 35)
        self.combo_user_upper = ComboBox(self.screen, self.user_names[0:8], self.rect_combo_user_upper, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Usuario")
        self.rect_combo_graph_upper = pygame.Rect(1211, 178, 177, 35)
        self.combo_graph_upper = ComboBox(self.screen, ["Red de amigos", "Red de familia", "Grupos y comunidades"], self.rect_combo_graph_upper, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Seleccione")
        self.rect_combo_friends_lower = pygame.Rect(1211, 366, 177, 35)
        self.combo_friends_lower = ComboBox(self.screen, [], self.rect_combo_friends_lower, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Amigo")
    
    def draw(self):
        self.isAcceptButtonClicked()
        
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_upper, 3)
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_lower, 3)
        
        # Draw lower part
        self.components.drawText("Seleccione un amigo", self.components.BLACK, None, 1216, 318, "Arial", 18, False)
        self.components.drawText("de la red del usuario", self.components.BLACK, None, 1218, 339, "Arial", 18, False)


        # Draw upper part

        # Title
        self.components.drawText("Seleccione un usuario", self.components.BLACK, None, 1211, 11, "Arial", 18, False)

        # Title
        self.components.drawText("Seleccione el grafo que", self.components.BLACK, None, 1205, 130, "Arial", 18, False)
        self.components.drawText("desea visualizar", self.components.BLACK, None, 1235, 151, "Arial", 18, False)

        # Accept button
        self.components.drawButton("Aceptar", self.components.GREEN, 1248, 235, 103, 30, 0, 11, 18, True, self.components.BLACK, "Arial")

        # Combo friends lower part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_friends_lower, 0, 7)
        self.combo_friends_lower.draw()

        # Combo graph upper part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_graph_upper, 0, 7)
        self.combo_graph_upper.draw()

        # Combo user upper part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_user_upper, 0, 7)
        self.combo_user_upper.draw()

    def isAcceptButtonClicked(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect_button_accept_upper.collidepoint(pygame.mouse.get_pos()) and not self.rect_button_accept_upper_clicked:
                self.rect_button_accept_upper_clicked = True
                if not self.combo_user_upper.combo_open and not self.combo_graph_upper.combo_open and not self.combo_friends_lower.combo_open:
                    user_selected = self.combo_user_upper.getValue()
                    friends = self.relationships[str(self.user_names.index(user_selected) + 1)]
                    data = list(filter(lambda x: x["id"] in friends, [user for user in self.users]))
                    names = [user["name"] for user in data]
                    self.combo_friends_lower.updateOptions(names)

        if not pygame.mouse.get_pressed()[0]:
            self.rect_button_accept_upper_clicked = False
        