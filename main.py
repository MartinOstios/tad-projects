from single_linked_list import *
import pygame
import sys
from alert import Alert
from footer import Footer
from menu import Menu
from combo_box import ComboBox
from components import Components
pygame.init()


class Superheroes:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Superheroes")
        self.BLACK = (0, 0,   0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (134, 181, 129)
        self.RED = (255, 0,   0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (170, 170, 170)
        self.LIGHT_BLUE = (161, 163, 212)
        self.sll = SingleLinkedList()
        self.imgs_dict = {}
        self.rect_combo_method = pygame.Rect(280, 109, 300, 37)
        self.rect_combo_position = pygame.Rect(887, 109, 180, 37)
        self.accept_button = pygame.Rect(504, 356, 191, 39)
        self.superheroes = ["spiderman", "america",
                            "batman", "flash", "ironman", "superman", "thor"]
        self.options = {
            "Agregar al principio": self.sll.create_node_sll_unshift,
            "Agregar al final": self.sll.create_node_sll_ends,
            "Agregar en posición": self.sll.add_node,
            "Eliminar último": self.sll.delete_node_sll_pop,
            "Eliminar primero": self.sll.shift_node_sll,
            "Eliminar en posición": self.sll.remove_node,
            "Actualizar elemento": self.sll.update_node_value,
            "Revertir": self.sll.reverse,
            "Limpiar": self.sll.delete_list
        }
        self.control = True
        self.alert = Alert(self.screen)
        self.alert_text = ""
        self.alert_status = 0

        self.components = Components(self.screen)
        self.footer = Footer(self.screen)
        self.menu = Menu(self.screen, {"SLL": "imgs/list-outline.png", "DLL": "imgs/list-outline.png", "Pilas y colas": "imgs/list-outline.png", "Árboles": "imgs/tree-solid.png", "Grafos": "imgs/circle-nodes-solid.png"}, self.GREEN, 50, "Consolas", 22, self.WHITE)
        self.combo_method_object = ComboBox(self.screen, list(self.options.keys()), self.rect_combo_method, self.BLACK, "Consolas", 22, 5, self.WHITE, self.WHITE, 40, "Seleccione")
        self.combo_position_object = ComboBox(self.screen, ["1"], self.rect_combo_position, self.BLACK, "Consolas", 22, 5, self.WHITE, self.WHITE, 40, "Seleccione")
    def run(self):
        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.control:
                        self.clickOnInitMain()
                    else:
                        self.clickOnMain()
                        self.clickOnButton()
            self.screen.fill(self.WHITE)
            if(self.menu.getSelectedOption() == 0):
                self.drawList()
                self.drawMain()
                
            self.menu.draw()
            self.footer.draw()
            if (self.alert.draw(self.components.getText("¡Alerta!", 32, True, self.WHITE, None, "Consolas"), self.components.getText(self.alert_text, 22, False, self.WHITE, None, "Consolas"), self.components.getText("Aceptar", 22, False, self.BLACK, None, "Consolas"), self.alert_status)):
                self.alert_status = 0
            pygame.display.flip()
    
    def saveImage(self, url, pos_x, pos_y):
        image = pygame.image.load(url)
        if len(self.imgs_dict) < 7:
            self.imgs_dict[url] = pygame.Rect(pos_x, pos_y, image.get_width(), image.get_height())

    def drawMain(self):
        avatar1 = "imgs/batman.png"
        avatar2 = "imgs/america.png"
        avatar3 = "imgs/spiderman.png"
        arrow_down_icon = "imgs/caret-down-outline.png"
        pygame.draw.rect(self.screen, self.BLACK, (0, 50, self.screen.get_width(), self.screen.get_height() - 50), 8)
        self.components.drawText("Single Linked List", self.BLACK, None, 491, 70, "Consolas", 22, True)
        if self.control:
            self.components.drawText("Para iniciar debes seleccionar al menos una", self.BLACK, None, 340, 125, "Consolas", 22, True)
            self.components.drawText("imagen que será cabeza de la lista", self.BLACK, None, 394, 151, "Consolas", 22, True)
            self.components.drawImage(avatar1, 328, 202)
            self.saveImage(avatar1, 328, 202)
            self.components.drawImage(avatar2, 544, 202)
            self.saveImage(avatar2, 544, 202)
            self.components.drawImage(avatar3, 760, 202)
            self.saveImage(avatar3, 760, 202)
        else:
            self.components.drawText("Seleccione un método: ", self.BLACK, None, 21, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.BLACK, self.rect_combo_method, 0, 5)
            self.components.drawImage(arrow_down_icon, 540, 114)
            self.components.drawText("Seleccione la posición: ", self.BLACK, None, 604, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.BLACK, self.rect_combo_position, 0, 5)
            self.components.drawImage(arrow_down_icon, 1030, 114)
            gap = 0
            for hero in self.superheroes:
                avatar = "imgs/" + hero + ".png"
                self.components.drawImage(avatar, 55 + gap, 159)
                self.saveImage(avatar, 55 + gap, 159)
                gap += 163
            self.components.drawButton("Aceptar", self.GREEN, 504, 356, 191, 39, 0, 16, 22, True, self.BLACK, "Consolas")
            self.combo_method_object.draw()
            self.combo_position_object.draw()

    def drawList(self):
        ext_rect = pygame.Rect(0, 412, self.screen.get_width(), 207)
        int_rect = pygame.Rect(21, 432, 1158, 169)
        pygame.draw.rect(self.screen, self.BLACK, ext_rect, 8)
        pygame.draw.rect(self.screen, self.GRAY, int_rect, 0, 34)
        list_size = self.sll.get_length()
        gap = 0
        for i in range(1, list_size + 1):
            node = self.sll.get_node(i)
            avatar = "imgs/" + node.value + ".png"
            self.components.drawImage(avatar, int_rect.x + gap, int_rect.y)
            gap += 150

    def clickOnInitMain(self):
        keys = list(self.imgs_dict.keys())
        values = list(self.imgs_dict.values())
        for rect in values:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.control = False
                name = keys[values.index(rect)]
                self.sll.create_node_sll_ends(name.split("/")[1].split(".")[0].capitalize())
                self.imgs_dict.clear()

    def clickOnMain(self):
        if not self.combo_method_object.getComboStatus() and not self.combo_position_object.getComboStatus():
            keys = list(self.imgs_dict.keys())
            values = list(self.imgs_dict.values())
            for rect in values:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    superhero_selected = self.getSelected()
                    if superhero_selected != None:
                        index_selected = self.superheroes.index(superhero_selected)
                        self.superheroes[index_selected] = self.superheroes[index_selected].split("_")[1]
                    name = keys[values.index(rect)]
                    index = self.superheroes.index(name.split("/")[1].split(".")[0])
                    self.superheroes[index] = "h_" + self.superheroes[index]
            # print(self.superheroes)

    def getSelected(self):
        for superhero in self.superheroes:
            if len(superhero.split("_")) > 1:
                return superhero
        return None

    def clickOnButton(self):
        if self.accept_button.collidepoint(pygame.mouse.get_pos()):
            if self.combo_method_object.getIndex() != -1:
                exec_func = self.options[self.combo_method_object.getValue()]
                arg_count = exec_func.__code__.co_argcount
                arg_names = exec_func.__code__.co_varnames[1:arg_count]
                superhero_selected = self.getSelected()
                if arg_count == 1:
                    exec_func()
                elif arg_count == 2:
                    if arg_names[0] == 'value':
                        if superhero_selected != None:
                            exec_func(superhero_selected.split("_")[1].capitalize())
                        else:
                            self.alert_status = 1
                            self.alert_text = "Seleccione un superheroe"
                    if arg_names[0] == 'index':
                        if self.combo_position_object.getIndex() != -1:
                            exec_func(int(self.combo_position_object.getValue()))
                        else:
                            self.alert_status = 1
                            self.alert_text = "Seleccione el índice"
                elif arg_count == 3:
                    if self.combo_method_object.getIndex() != -1 and superhero_selected != None:
                        exec_func(int(self.combo_position_object.getValue()), superhero_selected.split("_")[1].capitalize())
                    else:
                        self.alert_status = 1
                        self.alert_text = "Seleccione el índice y el superhéroe"
                self.resetForm()
                data_list = [str(x) for x in range(1, self.sll.get_length() + 1)]
                self.combo_position_object.updateOptions(data_list)
            else:
                self.alert_status = 1
                self.alert_text = "Seleccione un método primero"

    def resetForm(self):
        self.combo_method_object.resetCombo()
        self.combo_position_object.resetCombo()
        self.superheroes = ["spiderman", "america", "batman", "flash", "ironman", "superman", "thor"]


if __name__ == "__main__":
    a = Superheroes()
    a.run()
