#pip install --upgrade pygame
from io import BytesIO
import json
import random
import requests
import urllib.parse
import pygame
import networkx as nx
import matplotlib.pyplot as plt
from faker import Faker
from PIL import Image
from images_api import ImagesApi
from components import Components
from side_menu import SideMenu
pygame.init()
fake = Faker()
generator = ImagesApi()
class GraphView:
    def __init__(self):
        # Configuración de la ventana
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 600
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.users = {}
        self.relationships = {}
        self.node_positions = {}
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Red de Usuarios de Facebook")
        self.clock = pygame.time.Clock()
        self.components = Components(self.screen)
        self.load_json()
        self.set_positions()
        print(self.users)
        self.menu = SideMenu(self.screen, self.WINDOW_WIDTH - 200, 0, 200, self.WINDOW_HEIGHT, self.components.GRAY, self.users, self.relationships)

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
            self.relationships = data["relationships"]
            self.load_profile_images()

    def load_profile_images(self):
        for user in self.users:
            try:
                image = user["profile_image_url"]
                image = pygame.image.load(image)
                user["profile_image"] = image
            except Exception as e:
                print(f"Error al cargar la imagen de perfil para el usuario {user['id']}: {e}")

    def draw(self):
        # Dibujar las relaciones de amistad
        self.menu.draw()
        for user_id, friends in self.relationships.items():
            start_pos = self.node_positions.get(int(user_id))  # Verificar si la clave existe en node_positions
            if start_pos is not None:
                for friend_id in friends:
                    end_pos = self.node_positions.get(friend_id)  # Verificar si la clave existe en node_positions
                    if end_pos is not None:
                        pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)

        # Dibujar los nodos
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
        x_spacing = (self.WINDOW_WIDTH - 200) // (len(self.users) + 1)
        y_spacing = self.WINDOW_HEIGHT // (len(self.users) + 1)
        y_positions = [random.randint(y_spacing, self.WINDOW_HEIGHT - y_spacing) for _ in range(len(self.users))]
        for i, user in enumerate(self.users):
            x = (i + 1) * x_spacing
            y = y_positions[i]
            self.node_positions[user["id"]] = (x, y)

        '''
        # Restablecer la posición vertical de los nodos
        for user in self.users:
            pos = self.node_positions.get(user["id"])
            if pos is not None:
                _, y = pos
                # Obtener la posición original del nodo
                y = y_positions[user["id"] - 1]  
                self.node_positions[user["id"]] = (x, y)
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

def generate_profile_image():
    style = random.choice(["female", "male"])
    url = generator.get_image(style)
    return url


def generate_fake_data(num_users):
    users = []
    relationships = {}

    for i in range(num_users):
        try:
            name = fake.name()
            profile_image_url = generate_profile_image()
            user = {
                "id": i + 1,
                "name": name,
                "email": f"{name}@example.com",
                "birthdate": "1990-01-01",
                "profile_image_url": profile_image_url,
                "liked_photos": [],
                "family": [],
                "groups": [],
                "communities": []
            }
            users.append(user)
            num_family_members = 3
            num_family_members = min(num_family_members, len(users))
            family_members = random.sample(users, num_family_members)
            for family_member in family_members:
                if family_member["name"] != user["name"]:
                    member = {
                        "name": family_member["name"],
                        "relation": random.choice(["Father", "Mother", "Sibling"])
                    }
                else:
                    member = None
                if member is not None:
                    user["family"].append(member)
        except Exception as e:
            print(f"Error al generar el usuario {i + 1}: {e}")

    graph = nx.DiGraph()

    for user in users:
        graph.add_node(user["id"], data=user)

    for user in users:
        # ----------------- Cantidad de amigos -----------------------
        num_friends = random.randint(1, 5)
        #data = list(filter(lambda x: x["id"] in friends, [user for user in self.users]))
        friends = random.sample(users, num_friends)
        friends = filter(lambda x: not x["id"] == user["id"], friends)
        relationship_ids = [friend["id"] for friend in friends]
        relationships[user["id"]] = relationship_ids
        for friend in friends:
            graph.add_edge(user["id"], friend["id"])
    data = {
        "users": users,
        "relationships": relationships
    }

    return data, graph

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
        print("Relaciones de amistad:")
        for user_id, friends in data["relationships"].items():
            print("ID de usuario:", user_id)
            print("Amigos:", friends)
            print("------------------------")

    


if __name__ == "__main__":
    # Generar datos falsos y escribir el archivo JSON
    data, graph = generate_fake_data(5)
    write_json_file(data, "facebook_data.json")
    # Leer y mostrar los datos del archivo JSON
    read_facebook_data("facebook_data.json")
    # Ejecutar la función principal
    graph = GraphView()
    graph.run()
