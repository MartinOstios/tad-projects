import pygame
from single_linked_list import *
from components import Components
from alert import Alert
pygame.init()

class View():
    def __init__(self, screen):
        self.screen = screen
        self.sll = SingleLinkedList()
        self.imgs_dict = {}
        self.combo_method = pygame.Rect(280, 109, 300, 37)
        self.combo_method_selection = ""
        self.combo_position = pygame.Rect(887, 109, 156, 37)
        self.combo_position_selection = ""
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
        self.click_on_combo_method = False
        self.click_on_combo_position = False
        self.alert = Alert(self.screen)
        self.alert_text = ""
        self.alert_status = 0
        self.components = Components(self.screen)

    def drawMain(self):
        avatar1 = "imgs/batman.png"
        avatar2 = "imgs/america.png"
        avatar3 = "imgs/spiderman.png"
        arrow_down_icon = "imgs/caret-down-outline.png"
        pygame.draw.rect(self.screen, self.components.BLACK, (0, 50, self.screen.get_width(), self.screen.get_height() - 50), 8)
        self.components.drawText("Single Linked List", self.components.BLACK,None, 491, 70, "Consolas", 22, True)
        if self.control:
            self.components.drawText("Para iniciar debes seleccionar al menos una", self.components.BLACK, None, 340, 125, "Consolas", 22, True)
            self.components.drawText("imagen que será cabeza de la lista", self.components.BLACK, None, 394, 151, "Consolas", 22, True)
            self.components.drawImage(avatar1, 328, 202, True)
            self.components.drawImage(avatar2, 544, 202, True)
            self.components.drawImage(avatar3, 760, 202, True)
        else:
            self.drawText("Seleccione un método: ", self.BLACK, None, 21, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.combo_method, 0, 11)
            self.drawText(self.combo_method_selection, self.BLACK, None, self.combo_method.x + 10, self.combo_method.y + 7, "Consolas", 22, True)
            self.drawImage(arrow_down_icon, 540, 114)
            self.drawText("Seleccione la posición: ", self.BLACK, None, 604, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.combo_position, 0, 11)
            self.drawText(self.combo_position_selection, self.BLACK, None, self.combo_position.x + 10, self.combo_position.y + 7, "Consolas", 22, True)
            self.drawImage(arrow_down_icon, 1007, 114)
            gap = 0
            for hero in self.superheroes:
                avatar = "imgs/" + hero + ".png"
                self.drawImage(avatar, 55 + gap, 159, True)
                gap += 163
            self.drawButton("Aceptar", self.GREEN, 504, 356, 191, 39, 0, 16, 22, True, self.BLACK, "Consolas")

            if self.click_on_combo_method:
                self.drawSelectOption(self.combo_method, list(
                    self.options.keys()), 11, self.LIGHT_BLUE, "combo_method")
            if self.click_on_combo_position:
                data_list = [str(x) for x in range(1, self.sll.get_length() + 1)]
                self.drawSelectOption(
                    self.combo_position, data_list, 11, self.LIGHT_BLUE, "combo_position")

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
            self.drawImage(avatar, int_rect.x + gap, int_rect.y)
            gap += 150

    def clickOnInitMain(self):
        keys = list(self.imgs_dict.keys())
        values = list(self.imgs_dict.values())
        for rect in values:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.control = False
                name = keys[values.index(rect)]
                self.sll.create_node_sll_ends(
                    name.split("/")[1].split(".")[0].capitalize())
                self.imgs_dict.clear()

    def clickOnMain(self):
        if not self.click_on_combo_method and not self.click_on_combo_position:
            keys = list(self.imgs_dict.keys())
            values = list(self.imgs_dict.values())
            for rect in values:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    superhero_selected = self.getSelected()
                    if superhero_selected != None:
                        index_selected = self.superheroes.index(superhero_selected)
                        self.superheroes[index_selected] = self.superheroes[index_selected].split("_")[1]
                    name = keys[values.index(rect)]
                    index = self.superheroes.index(
                        name.split("/")[1].split(".")[0])
                    self.superheroes[index] = "h_" + self.superheroes[index]
            # print(self.superheroes)

    def getSelected(self):
        for superhero in self.superheroes:
            if len(superhero.split("_")) > 1:
                return superhero
        return None

    def clickOnMethodCombo(self):
        if self.combo_method.collidepoint(pygame.mouse.get_pos()):
            self.click_on_combo_method = True
        if self.combo_position.collidepoint(pygame.mouse.get_pos()):
            self.click_on_combo_position = True

    def clickOnButton(self):
        if self.accept_button.collidepoint(pygame.mouse.get_pos()):
            if self.combo_method_selection != "":
                exec_func = self.options[self.combo_method_selection]
                arg_count = exec_func.__code__.co_argcount
                arg_names = exec_func.__code__.co_varnames[1:arg_count]
                superhero_selected = self.getSelected()
                if arg_count == 1:
                    exec_func()
                elif arg_count == 2:
                    if arg_names[0] == 'value':
                        if superhero_selected != None:
                            exec_func(superhero_selected.split(
                                "_")[1].capitalize())
                        else:
                            self.alert_status = 1
                            self.alert_text = "Seleccione un superheroe"
                    if arg_names[0] == 'index':
                        if self.combo_position_selection != "":
                            exec_func(int(self.combo_position_selection))
                        else:
                            self.alert_status = 1
                            self.alert_text = "Seleccione el índice"
                elif arg_count == 3:
                    if self.combo_position_selection != "" and superhero_selected != None:
                        exec_func(int(self.combo_position_selection), superhero_selected.split("_")[1].capitalize())
                    else:
                        self.alert_status = 1
                        self.alert_text = "Seleccione el índice y el superhéroe"
                self.resetForm()
            else:
                self.alert_status = 1
                self.alert_text = "Seleccione un método primero"

    def resetForm(self):
        self.combo_method_selection = ""
        self.combo_position_selection = ""
        self.superheroes = ["spiderman", "america",
                            "batman", "flash", "ironman", "superman", "thor"]