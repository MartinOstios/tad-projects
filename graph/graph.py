#pip install --upgrade pygame
from io import BytesIO
import json
import random
import requests
import urllib.parse
from datetime import datetime, timedelta
import pygame
import networkx as nx
import matplotlib.pyplot as plt
from faker import Faker
from PIL import Image
from images_api import ImagesApi
from components import Components
from side_menu import SideMenu
from drawer import Drawer
pygame.init()
fake = Faker("es_CO")
generator = ImagesApi()


class GraphView:
    def __init__(self):
        self.USERS_QUANTITY = 20
        self.FRIENDS_QUANTITY = 3
        self.FAMILY_QUANTITY = 3
        self.generate_data()
        # Configuración de la ventana
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 600
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.users = {}
        self.relationships = {}
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Red de Usuarios de Facebook")
        self.clock = pygame.time.Clock()
        self.components = Components(self.screen)
        self.load_json()
        self.drawer = Drawer(self.screen, 0, 0, self.WINDOW_WIDTH - 200, self.WINDOW_HEIGHT, self.users)
        self.menu = SideMenu(self.screen, self.WINDOW_WIDTH - 200, 0, 200, self.WINDOW_HEIGHT, self.components.GRAY, self.users, self.relationships, self.drawer)

    def run(self):
        while True:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Actualizar la ventana
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def load_json(self):
        # Leer y cargar los datos del archivo JSON
        with open("facebook_data.json", "r") as file:
            data = json.load(file)
            self.users = data["users"]
            #self.relationships = data["relationships"]
            self.load_profile_images()

    def load_profile_images(self):
        for user in self.users:
            try:
                image = user["profile_image_url"]
                image = pygame.image.load(image)
                user["profile_image"] = image
                for friend in user["friends"]:
                    image = friend["profile_image_url"]
                    image = pygame.image.load(image)
                    friend["profile_image"] = image
                    
                for family in user["family"]:
                    image = family["profile_image_url"]
                    image = pygame.image.load(image)
                    family["profile_image"] = image

            except Exception as e:
                print(f"Error al cargar la imagen de perfil para el usuario {user['id']}: {e}")

    def draw(self):
        self.components.drawImage("graph/imgs/logo-facebook.png", 18, 12)
        self.components.drawText("Estos datos son fake y se leen a través de un archivo JSON", self.components.BLACK, None, 94, 35, "Arial", 16, False)
        self.menu.draw()
        self.drawer.draw()
    
    def generate_data(self):
        # Generar datos falsos y escribir el archivo JSON
        data, graph = self.generate_fake_data(self.USERS_QUANTITY)
        write_json_file(data, "facebook_data.json")
        # Leer y mostrar los datos del archivo JSON
        read_facebook_data("facebook_data.json")

        #pos = nx.spring_layout(graph)
        #nx.draw(graph, with_labels=True)
        #plt.show()
        # Ejecutar la función principal
    
    def generate_profile_image(self):
        style = random.choice(["female", "male"])
        url = generator.get_image(style)
        return url
    
    def generate_email(self, name):
        return name.split(" ")[0] + "_" + name.split(" ")[1] + "@" + random.choice(["gmail.com", "hotmail.com", "autonoma.edu.co", "yahoo.com"])

    def generate_date(self, start, end, fmt):
        s = datetime.strptime(start, fmt)
        e = datetime.strptime(end, fmt)

        delta = e - s

        return s + timedelta(days=(random.random() * delta.days))
    
    def generate_fake_data(self, num_users):
        users = []
        graph = nx.DiGraph()
        for i in range(num_users):
            try:
                name = fake.name()
                profile_image_url = self.generate_profile_image()
                email = self.generate_email(name.lower())
                date = self.generate_date("01/01/1970", "01/01/2010", "%d/%m/%Y")
                date = str(date).split(" ")[0]
                user = {
                    "id": i + 1,
                    "name": name,
                    "email": email,
                    "birthdate": date,
                    "profile_image_url": profile_image_url,
                    "liked_photos": [],
                    "friends": [],
                    "family": [],
                    "groups": [],
                    "communities": []
                }
                users.append(user)
                graph.add_node(user["id"], data=user)

                num_friends = random.randint(1, self.FRIENDS_QUANTITY)
                num_friends = min(num_friends, len(users))
                friends = random.sample(users, num_friends)
                for friend in friends:
                    if friend != user:
                        user["friends"].append({
                            "id": friend["id"],
                            "name": friend["name"],
                            "profile_image_url": friend["profile_image_url"]
                        })
                        friend["friends"].append({
                            "id": user["id"],
                            "name": user["name"],
                            "profile_image_url": user["profile_image_url"]
                        })
                        graph.add_edge(user["id"], friend["id"])

                num_family_members = self.FAMILY_QUANTITY
                num_family_members = min(num_family_members, len(users))
                family_members = random.sample(users, num_family_members)
                for family_member in family_members:
                    if family_member["name"] != user["name"]:
                        user["family"].append({
                            "id": family_member["id"],
                            "name": family_member["name"],
                            "profile_image_url": family_member["profile_image_url"],
                            "relation": random.choice(["Father", "Mother", "Sibling"])
                        })
                        # 3.b
                        family_member["family"].append({
                            "id": user["id"],
                            "name": user["name"],
                            "profile_image_url": user["profile_image_url"],
                            "relation": "Familiar"
                        })
                
                

            except Exception as e:
                print(f"Error al generar el usuario {i + 1}: {e}")


        
        '''
            for user in users:
            # ----------------- Cantidad de amigos -----------------------
            num_friends = random.randint(1, self.FRIENDS_QUANTITY)
            friends = random.sample(users, num_friends)
            # Filtrar la lista para que no se añada a si mismo como amigo
            relationship_ids = list(filter(lambda x: not x == user["id"], [friend["id"] for friend in friends]))
            relationships[user["id"]] = relationship_ids
            for friend in friends:
                graph.add_edge(user["id"], friend["id"])
        '''

        data = {
            "users": users,
        }

        return data, graph


'''
def generate_profile_image_url(name):
    # Generar una URL de imagen de perfil falsa con un avatar generado
    style = random.choice(["female", "male"])
    encoded_name = urllib.parse.quote(name)
    url = f"https://avatars.dicebear.com/api/{style}/{encoded_name}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al generar la imagen de perfil: {response.status_code}")
    content_type = response.headers.get("content-type")
    if "image" not in content_type:
        raise Exception("La respuesta no es una imagen válida.")
    return url
'''




def write_json_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    print(f"El archivo {filename} ha sido creado exitosamente.")

def read_facebook_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

        # Leer usuarios
        print("Usuarios:")
        for user in data["users"]:
            print("ID:", user["id"])
            print("Nombre:", user["name"])
            print("Email:", user)
            print("Fecha de nacimiento:", user["birthdate"])
            print("URL de imagen de perfil:", user["profile_image_url"])
            print("Miembros de la familia:")
            for family_member in user["family"]:
                print("Nombre:", family_member["name"])
                print("Relación:", family_member["relation"])
            print("------------------------")

        # Leer relaciones de amistad
        #print("Relaciones de amistad:")
        #for user_id, friends in data["relationships"].items():
            #print("ID de usuario:", user_id)
            #print("Amigos:", friends)
            #print("------------------------")

    


if __name__ == "__main__":
    graph = GraphView()
    graph.run()
