import random
class CardPool:
    def __init__(self):
        self.card_quantity = 52
        self.colors = ["red", "black"]
        self.symbols = ["heart", "tiles", "clover", "pikes"]
        self.characters = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
        self.pool = {}
        self.boolean_test = True
        self.fill_pool()

    def fill_pool(self):
        colors_number = 0
        symbols_number = 0
        character_number = 0
        for i in range(self.card_quantity):
            self.pool[i] = [self.characters[character_number], self.colors[colors_number], self.symbols[symbols_number], 0]
            if i == 25:
                colors_number += 1
            character_number += 1
            if character_number == 13:
                symbols_number += 1
                character_number = 0
    
    def get_random_card(self):
        rand_num = random.randint(0, self.card_quantity - 1)
        if self.pool[rand_num][3] != 1:
            self.pool[rand_num][3] = 1
            return self.pool[rand_num]
        else:
            return self.get_random_card()  

