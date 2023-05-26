from components import Components
import pygame
from combo_box import ComboBox
class SideMenu:
    def __init__(self, screen, x, y, width, height, color, users, communities, drawer):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.users = users
        self.communities = communities
        self.drawer = drawer
        self.user_names = [str(user["name"]) for user in self.users]
        self.color = color
        self.components = Components(self.screen)
        self.rect_button_accept_upper = pygame.Rect(1248, 235, 103, 30)
        self.rect_button_accept_upper_clicked = False
        self.rect_button_accept_lower = pygame.Rect(1248, 553, 103, 30)
        self.rect_button_accept_lower_clicked = False
        self.rect_upper = pygame.Rect(x, y, self.width, self.height/2)
        self.rect_lower = pygame.Rect(x, y + self.height/2, self.width, self.height/2)
        self.rect_combo_user_upper = pygame.Rect(1211, 38, 177, 35)
        # La cantidad de nombres que se muestra está limitada a 8
        self.combo_user_upper = ComboBox(self.screen, self.user_names[0:8], self.rect_combo_user_upper, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Usuario")
        self.rect_combo_graph_upper = pygame.Rect(1211, 178, 177, 35)
        self.combo_graph_upper = ComboBox(self.screen, ["Red de amigos", "Red de familia", "Red de comunidades"], self.rect_combo_graph_upper, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Seleccione")
        self.rect_combo_friends_lower = pygame.Rect(1211, 366, 177, 35)
        self.combo_friends_lower = ComboBox(self.screen, [], self.rect_combo_friends_lower, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Amigo")
        self.rect_combo_graph_lower = pygame.Rect(1211, 477, 177, 35)
        self.combo_graph_lower = ComboBox(self.screen, ["Comunidades en común"], self.rect_combo_graph_lower, self.components.BLACK, "Arial", 15, 7, self.components.WHITE, self.components.WHITE, 30, "Seleccione")
    
    def draw(self):
        self.isAcceptButtonUpperClicked()
        self.isAcceptButtonLowerClicked()
        
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_upper, 3)
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_lower, 3)
        
        # Draw lower part
        self.components.drawText("Seleccione un amigo", self.components.BLACK, None, 1216, 318, "Arial", 18, False)
        self.components.drawText("de la red del usuario", self.components.BLACK, None, 1218, 339, "Arial", 18, False)

        # Title
        self.components.drawText("Seleccione el grafo que", self.components.BLACK, None, 1205, 429, "Arial", 18, False)
        self.components.drawText("desea visualizar", self.components.BLACK, None, 1235, 450, "Arial", 18, False)

        # Draw upper part

        # Title
        self.components.drawText("Seleccione un usuario", self.components.BLACK, None, 1211, 11, "Arial", 18, False)

        # Title
        self.components.drawText("Seleccione el grafo que", self.components.BLACK, None, 1205, 130, "Arial", 18, False)
        self.components.drawText("desea visualizar", self.components.BLACK, None, 1235, 151, "Arial", 18, False)

        # Accept button upper
        self.components.drawButton("Aceptar", self.components.GREEN, 1248, 235, 103, 30, 0, 11, 18, True, self.components.BLACK, "Arial")

        # Accept button lower
        self.components.drawButton("Aceptar", self.components.GREEN, 1248, 553, 103, 30, 0, 11, 18, True, self.components.BLACK, "Arial")

        # Combo graph lower part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_graph_lower, 0, 7)
        self.combo_graph_lower.draw()

        # Combo friends lower part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_friends_lower, 0, 7)
        self.combo_friends_lower.draw()

        # Combo graph upper part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_graph_upper, 0, 7)
        self.combo_graph_upper.draw()

        # Combo user upper part
        pygame.draw.rect(self.screen, self.components.BLACK, self.rect_combo_user_upper, 0, 7)
        self.combo_user_upper.draw()

    def isAcceptButtonUpperClicked(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect_button_accept_upper.collidepoint(pygame.mouse.get_pos()) and not self.rect_button_accept_upper_clicked:
                self.rect_button_accept_upper_clicked = True
                if not self.combo_user_upper.combo_open and not self.combo_graph_upper.combo_open and not self.combo_friends_lower.combo_open and not self.combo_graph_lower.combo_open:
                    if self.combo_user_upper.getIndex() != -1:
                        # Obtiene el valor del combo
                        user_selected = self.combo_user_upper.getIndex()
                        self.updateComboFriends(user_selected)
                        if self.combo_graph_upper.getIndex() != -1:
                            graph_selected = self.combo_graph_upper.getIndex()
                            self.updateGraph(user_selected, graph_selected)
                        else:
                            print("Seleccione tipo de grafo")
                    else:
                        print("Seleccione un usuario")

        if not pygame.mouse.get_pressed()[0]:
            self.rect_button_accept_upper_clicked = False
    
    def isAcceptButtonLowerClicked(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect_button_accept_lower.collidepoint(pygame.mouse.get_pos()) and not self.rect_button_accept_lower_clicked:
                self.rect_button_accept_lower_clicked = True
                if not self.combo_user_upper.combo_open and not self.combo_graph_upper.combo_open and not self.combo_friends_lower.combo_open and not self.combo_graph_lower.combo_open:
                    print("Click accept de abajo")
                    if self.combo_friends_lower.getIndex() != -1:
                        # Obtiene el valor del combo
                        user_selected = self.combo_user_upper.getIndex()
                        friend_selected = self.combo_friends_lower.getIndex()
                        if self.combo_graph_lower.getIndex() != -1:
                            graph_selected = self.combo_graph_lower.getIndex()
                            self.updateGraphCommunities(user_selected, friend_selected, graph_selected)
                        else:
                            print("Seleccione tipo de grafo")
                    else:
                        print("Seleccione un amigo")

        if not pygame.mouse.get_pressed()[0]:
            self.rect_button_accept_lower_clicked = False
    
    def updateComboFriends(self, user_selected):
        # Obtiene la lista de amigos del usuario seleccionado
        user = self.users[user_selected]
        friends = user["friends"]
        names = [friend["name"] for friend in friends]
        self.combo_friends_lower.updateOptions(names[0:6]) # Limitado a 6 amigos en la lista
    
    def updateGraph(self, user, graph):
        print(f"Se debe dibujar el grafo {graph} respecto al usuario {user}")
        if graph == 0:
            print("Red de amigos")
            self.getFriendNetwork(user)
        if graph == 1:
            print("Red de familia")
            self.getFamilyNetwork(user)
        if graph == 2:
            print("Comunidades que sigue")
            self.getCommunitiesNetwork(user)
    
    def getFriendNetwork(self, user_id):
        user = self.users[user_id]
        friends = user["friends"]
        self.drawer.set_data([user] + friends, "friends")
    
    def getFamilyNetwork(self, user_id):
        user = self.users[user_id]
        family = user["family"]
        self.drawer.set_data([user] + family, "family")
    
    def getCommunitiesNetwork(self, user_id):
        user = self.users[user_id]
        communities = user["communities"]
        print(communities)
        self.drawer.set_data([user] + communities, "communities")

        '''
        relationships = {}
        user = self.users[user_id]
        id_family = [family['id'] for family in user['family']]
        family = list(filter(lambda x: x["id"] in id_family, [user for user in self.users]))
        relationships[user["id"]] = id_family
        self.drawer.set_data([user] + family, relationships)
        '''
    
    def updateGraphCommunities(self, user1, user2, graph):
        print(f"Se debe dibujar el grafo {graph} respecto a los usuarios: {user1} - {user2}")
        if graph == 0:
            print("Comunidades en común")
            self.getInCommonCommunitiesNetwork(user1, user2)
    
    def getInCommonCommunitiesNetwork(self, user_id_1, user_id_2):
        common_communities = []
        user = self.users[user_id_1]
        friend = user["friends"][user_id_2]
        friend = self.users[friend["id"] - 1]
        print(user)
        print("-----------------------------")
        print(friend)
        print("-----------------")
        #print(self.communities)
        for communitie in self.communities:
            member1 = False
            member2 = False
            members = communitie["members"]
            print(f"Nombre comunidad: {communitie['name']}")
            for member in members:
                if member['name'] == user['name']:
                    member1 = True
                    print("Se encuentra el usuario 1")
                if member['name'] == friend['name']:
                    member2 = True
                    print("Se encuentra el usuario 2")
            print("---------------------------------")
            if member1 and member2:
                print(f"Ambos usuarios se encuentran en la comunidad {communitie['name']}")
                common_communities.append(communitie)
        print(common_communities)

        self.drawer.set_data([user] + [friend] + common_communities, "communities")