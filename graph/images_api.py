import random
class ImagesApi():
    def __init__(self):
        self.gender = ""
        self.images = []
        self.quantity = 19
        self.fill()

    def fill(self):
        self.images = [int(x) for x in range(1, self.quantity)]

    def get_image(self, gender):
        image_id = random.choice(self.images)
        url = f"graph/imgs/{gender}/{image_id}.png"
        return url

