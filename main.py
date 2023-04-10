from single_linked_list import *
import pygame
import sys
import webbrowser
from alert import Alert
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
        self.buttons_dict = {}
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
        self.clickable_components = {}
        self.control = True
        self.click_on_combo_method = False
        self.click_on_combo_position = False
        self.git_button_clicked = False
        self.alert = Alert(self.screen)
        self.alert_text = ""
        self.alert_status = 0

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
                        self.clickOnMethodCombo()
                        self.clickOnButton()
            self.screen.fill(self.WHITE)
            self.drawList()
            self.drawNav()
            self.drawFooter()
            self.drawMain()
            if (self.alert.draw(self.getText("¡Alerta!", 32, True, self.WHITE, None, "Consolas"), self.getText(self.alert_text, 22, False, self.WHITE, None, "Consolas"), self.getText("Aceptar", 22, False, self.BLACK, None, "Consolas"), self.alert_status)):
                self.alert_status = 0
            pygame.display.flip()

    def getText(self, text, size, bold, color, background_color, font_type):
        font = pygame.font.SysFont(font_type, size, bold)
        render_text = font.render(text, True, color, background_color)
        return render_text

    def drawText(self, text, color, background, pos_x, pos_y, font_type, size, bold):
        self.screen.blit(self.getText(text, size, bold, color,
                         background, font_type), (pos_x, pos_y))

    def drawImage(self, url, pos_x, pos_y, save=None):
        image = pygame.image.load(url)
        self.screen.blit(image, (pos_x, pos_y))
        if save and len(self.imgs_dict) < 7:
            self.imgs_dict[url] = pygame.Rect(
                pos_x, pos_y, image.get_width(), image.get_height())

    def drawButton(self, text, button_color, pos_x, pos_y, width, height, border, border_radius, text_size, text_bold, text_color, text_font):
        background_rect = pygame.Rect(pos_x, pos_y, width, height)
        pygame.draw.rect(self.screen, button_color,
                         background_rect, border, border_radius)
        render_text = self.getText(
            text, text_size, text_bold, text_color, None, text_font)
        self.screen.blit(render_text, (background_rect.x + (background_rect.width - render_text.get_width()
                                                            )/2, background_rect.y + (background_rect.height - render_text.get_height())/2))
        self.buttons_dict[text] = background_rect

    def drawSelectOption(self, rect, options_list, border_radius, color, combo_name):
        select_dict = {}
        select_rect = pygame.Rect(
            rect.x, rect.y, rect.width, rect.height + (31 * len(options_list)))
        pygame.draw.rect(self.screen, color, select_rect, 0, border_radius)
        gap = 0
        for option in options_list:
            self.drawText(option, self.BLACK, None, rect.x + 5,
                          rect.y + rect.height + gap + 5, "Consolas", 22, False)
            pygame.draw.line(self.screen, self.BLACK, (rect.x, rect.y + rect.height +
                             gap), (rect.x + rect.width, rect.y + rect.height + gap), 3)
            select_dict[option] = pygame.Rect(
                rect.x, rect.y + rect.height + gap, rect.width, 31)
            gap += 31
        if select_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == True:
            dict_values = list(select_dict.values())
            dict_keys = list(select_dict.keys())
            for value in dict_values:
                if value.collidepoint(pygame.mouse.get_pos()):
                    if combo_name == "combo_method":
                        self.combo_method_selection = dict_keys[dict_values.index(
                            value)]
                        self.click_on_combo_method = False
                    if combo_name == "combo_position":
                        self.combo_position_selection = dict_keys[dict_values.index(
                            value)]
                        self.click_on_combo_position = False
        if not select_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == True:
            self.click_on_combo_method = False
            self.click_on_combo_position = False

    def drawNav(self):
        list_icon = "imgs/list-outline.png"
        tree_icon = "imgs/tree-solid.png"
        arrow_down_icon = "imgs/caret-down-outline.png"
        node_icon = "imgs/circle-nodes-solid.png"
        pygame.draw.rect(self.screen, self.GRAY,
                         (0, 0, self.screen.get_width(), 50))
        self.drawImage(list_icon, 29, 10)
        self.drawText("SLL", self.BLACK, None, 62, 11, "Verdana", 20, False)
        self.drawImage(list_icon, 211, 10)
        self.drawText("DLL", self.BLACK, None, 243, 11, "Verdana", 20, False)
        self.drawImage(list_icon, 421, 10)
        self.drawText("PILAS Y COLAS", self.BLACK, None,
                      454, 11, "Verdana", 20, False)
        self.drawImage(tree_icon, 717, 10)
        self.drawText("ÁRBOLES", self.BLACK, None,
                      751, 11, "Verdana", 20, False)
        self.drawImage(arrow_down_icon, 852, 11)
        self.drawImage(node_icon, 958, 10)
        self.drawText("GRAFOS", self.BLACK, None,
                      996, 11, "Verdana", 20, False)
        self.drawImage(arrow_down_icon, 1097, 11)

    def drawMain(self):
        avatar1 = "imgs/batman.png"
        avatar2 = "imgs/america.png"
        avatar3 = "imgs/spiderman.png"
        arrow_down_icon = "imgs/caret-down-outline.png"
        pygame.draw.rect(self.screen, self.BLACK, (0, 50,
                         self.screen.get_width(), self.screen.get_height() - 50), 8)
        self.drawText("Single Linked List", self.BLACK,
                      None, 491, 70, "Consolas", 22, True)
        if self.control:
            self.drawText("Para iniciar debes seleccionar al menos una",
                          self.BLACK, None, 340, 125, "Consolas", 22, True)
            self.drawText("imagen que será cabeza de la lista",
                          self.BLACK, None, 394, 151, "Consolas", 22, True)
            self.drawImage(avatar1, 328, 202, True)
            self.drawImage(avatar2, 544, 202, True)
            self.drawImage(avatar3, 760, 202, True)
        else:
            self.drawText("Seleccione un método: ", self.BLACK,
                          None, 21, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE,
                             self.combo_method, 0, 11)
            self.drawText(self.combo_method_selection, self.BLACK, None,
                          self.combo_method.x + 10, self.combo_method.y + 7, "Consolas", 22, True)
            self.drawImage(arrow_down_icon, 540, 114)
            self.drawText("Seleccione la posición: ", self.BLACK,
                          None, 604, 117, "Consolas", 22, False)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE,
                             self.combo_position, 0, 11)
            self.drawText(self.combo_position_selection, self.BLACK, None,
                          self.combo_position.x + 10, self.combo_position.y + 7, "Consolas", 22, True)
            self.drawImage(arrow_down_icon, 1007, 114)
            gap = 0
            for hero in self.superheroes:
                avatar = "imgs/" + hero + ".png"
                self.drawImage(avatar, 55 + gap, 159, True)
                gap += 163
            self.drawButton("Aceptar", self.GREEN, 504, 356, 191,
                            39, 0, 16, 22, True, self.BLACK, "Consolas")

            if self.click_on_combo_method:
                self.drawSelectOption(self.combo_method, list(
                    self.options.keys()), 11, self.LIGHT_BLUE, "combo_method")
            if self.click_on_combo_position:
                data_list = [str(x)
                             for x in range(1, self.sll.get_length() + 1)]
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

    def drawFooter(self):
        git_icon = "imgs/logo-github.png"
        uam_icon = "imgs/logo-universidad.png"
        pygame.draw.rect(self.screen, self.BLACK,
                         (0, 613, self.screen.get_width(), 87))
        self.drawText("Desarrollado por:", self.WHITE,
                      None, 419, 633, "Arial", 20, True)
        self.drawText("Martin Ostios Arias", self.WHITE,
                      None, 593, 633, "Arial", 20, False)
        self.drawText("@ I SEM  - 2023", self.WHITE,
                      None, 512, 660, "Arial", 20, False)
        self.drawImage(git_icon, 787, 619)
        self.drawImage(uam_icon, 1037, 613)
        git_rect = pygame.Rect(787, 619, 70, 70)

        if git_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == True and not self.git_button_clicked:
                webbrowser.open(r"https://github.com/MartinOstios")
                self.git_button_clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.git_button_clicked = False

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
                        index_selected = self.superheroes.index(
                            superhero_selected)
                        self.superheroes[index_selected] = self.superheroes[index_selected].split("_")[
                            1]
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


if __name__ == "__main__":
    a = Superheroes()
    a.run()
