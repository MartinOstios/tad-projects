import pygame
from components import Components
from solitaire.stack import Stack
from solitaire.card_pool import CardPool
pygame.init()
class SolitaireView():
    def __init__(self, screen):
        self.screen = screen
        self.components = Components(self.screen)
        self.stacks = []
        self.card_pool = CardPool()
        self.create_stacks()
        self.stack_released = None
        self.stack_pressed = None
        self.card_pressed = None
        self.clicked = False
        self.movable = False
        self.reset_button = pygame.Rect(1026, 105, 140, 40)
        self.reset_button_clicked = False
        
    
    def create_stacks(self):
        gap = 0
        for i in range(1, 8):
            new_stack = Stack(self.screen, i, 31 + gap, 181, i, self.card_pool)
            self.stacks.append(new_stack)
            gap += 169

    def draw(self):
        self.drawMain()

    def drawMain(self):
        pygame.draw.rect(self.screen, self.components.BLACK, (0, 50, self.screen.get_width(), self.screen.get_height() - 50), 8)
        self.components.drawText("Solitaire", self.components.BLACK, None, 545, 70, "Consolas", 22, True)
        self.move_card()
        self.reset()
        for stack in self.stacks:
            stack.draw()
            if stack.stack_pressed():
                self.clicked = True
                self.movable = True
                self.card_pressed = stack.card_pressed
                self.stack_pressed = stack
            stack.set_clicked(self.clicked)
            if stack.stack_released():
                self.stack_released = stack
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        self.components.drawButton("Reiniciar", self.components.BLUE, 1026, 105, 140, 40, 0, 5, 22, False, self.components.BLACK, "Consolas")

    def move_card(self):
        if not self.clicked and self.movable:
            if self.card_pressed is not None:
                if self.card_pressed.head:
                    #print("=================================================================")
                    #print("La carta seleccionada está en el stack: " + str(self.card_pressed.stack_number))
                    #print("Es la carta número: " + str(self.card_pressed.character))
                    if self.stack_released is not None and self.stack_pressed is not None and self.stack_released != self.stack_pressed:
                        #print("El stack al que se quiere mover la carta es el: " + str(self.stack_released.stack_number))
                        self.stack_released.add_new_card(self.card_pressed)
                        self.stack_pressed.remove_card(self.card_pressed)

            #print("=======Cartas de los stacks=======")
            #for stack in self.stacks:
                #print("Stack: " + str(stack.stack_number) + " Cantidad de cartas: " + str(len(stack.cards)))
                #print(stack.cards)
            self.movable = False
            self.stack_released = None
            self.stack_pressed = None
            self.card_pressed = None
    
    def reset(self):
        if pygame.mouse.get_pressed()[0]:
            if self.reset_button.collidepoint(pygame.mouse.get_pos()) and not self.reset_button_clicked:
                self.__init__(self.screen)
                self.reset_button_clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.reset_button_clicked = False