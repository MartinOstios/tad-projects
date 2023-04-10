class SingleLinkedList:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def menu(self):
        # >>> Objetos de prueba <<<
        while True:
            try:
                opciones = {
                    '1': ('Agregar elemento al principio', self.create_node_sll_unshift),
                    '2': ('Agregar elemento al final', self.create_node_sll_ends),
                    '3': ('Eliminar el primer elemento', self.shift_node_sll),
                    '4': ('Eliminar el último elemento', self.delete_node_sll_pop),
                    '5': ('Obtener el tamaño', self.get_length), 
                    '6': ('Buscar posición de un elemento', self.search_index_node),
                    '7': ('Devolver elemento de una posición determinada', self.get_node_value),
                    '8': ('Invertir', self.reverse),
                    '9': ('Eliminar todos los elementos', self.delete_list),
                    '10': ('Ordenar', self.sort_list),
                    '11': ('Eliminar un elemento en una posición determinada', self.remove_node),
                    '12': ('Insertar un elemento en una posición determinada', self.add_node),
                    '13': ('Actualizar elemento dada una posición', self.update_node_value),
                    '14': ('Comprobar si la lista está vacía', self.is_empty),
                    '15': ("Mostrar Lista", self.show_list)
                    
                }
                print("\n >>> Menú SLL <<<")
                for clave in opciones:
                    print(f"[{clave}] {opciones[clave][0]}")
                print(f"[{len(opciones) + 1}] Salir")
                opcion = input("Opción: ")
                print("")

                if int(opcion) != len(opciones) + 1 and opcion in opciones:
                    opciones[opcion][1]()
                else:
                    print("Mensaje salida")
                    break;
            except ValueError:
                print(" ¡Error!: Debe ingresar un número")

    # Por fuera de la clase nodo
    def __init__(self):
        self.head = None
        self.tail = None
        self.max_length = 8
        self.length = 0

    def show_list(self):
        #1. Declarar un array(lista) vacía que contendrá los valores de los nodos de SLL
        array_with_nodes_value = list()
        current_node = self.head
        # Mientras el nodo actual que estoy visitando sea diferente de None
        while(current_node != None):
            # Añadir al final de la lista el valor extraido del nodo
            array_with_nodes_value.append(current_node.value)
            # Pasamos del nodo actual al siguiente nodo mediante el puntero
            current_node = current_node.next
        #Imprimimos los valores de la lista
        print(f"Lista: {array_with_nodes_value}")
        
    
    def create_node_sll_ends(self, value):
        if self.length != self.max_length:
            new_node = self.Node(value)
            if self.head == None:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
            self.length += 1
            self.show_list()
            return True
        return False

    def create_node_sll_unshift(self, value):
        if self.length != self.max_length:
            new_node = self.Node(value)
            if self.head == None:
                self.head = new_node
                self.tail = new_node
            else:
                new_node.next = self.head
                self.head = new_node
            self.length += 1
            self.show_list()
            return True
        return False
    
    def delete_node_sll_pop(self):
        print("\n >>>>>> Eliminando último nodo <<<<<< ")
        if self.length == 0:
            print("Lista vacía: no hay nodos por eliminar")
        elif self.length == 1:
            print(f"Valor del nodo a eliminar es: {self.tail.value}")
            self.head = None
            self.tail = None
            self.length = 0
        else:
            current_node = self.head
            new_tail = current_node
            while current_node.next != None:
                new_tail = current_node
                current_node = current_node.next
                
            
            print(f"Valor del nodo a eliminar es: {current_node.value}")
            self.tail = new_tail
            self.tail.next = None
            self.length -= 1

    def shift_node_sll(self):
        print("\n >>>>>> Eliminando primer nodo <<<<<< ")

        if self.length == 0:
            print(">> Lista vacía no hay nodos por eliminar <<")
        elif self.length == 1:
            print(f"Valor del nodo a eliminar es: {self.head.value}")
            self.head = None
            self.tail = None
            self.length = 0
        else:
            remove_node = self.head
            print(f'Valor del nodo a eliminar es: {remove_node.value}')
            self.head = remove_node.next
            remove_node.next = None 
            self.length -=1

    def get_node(self, index):
        # Pedir valor del nodo
        # index = input("Ingrese el índice del nodo que desea obtener: ")

        if index < 1 or index > self.length:
            return None
        elif index == 1:
            return self.head
        elif index == self.length:
            return self.tail
        else:
            current_node = self.head
            node_counter = 1
            while(index != node_counter):
                current_node = current_node.next
                node_counter +=1
            return current_node
    
    def get_node_value(self, index):
        # Pedir valor del nodo

        if index < 1 or index > self.length:
            print("Nodo no encontrado")
        elif index == 1:
            print("El valor es: ", self.head.value)
        elif index == self.length:
            print("El valor es: ", self.tail.value)
        else:
            current_node = self.head
            node_counter = 1
            while(index != node_counter):
                current_node = current_node.next
                node_counter +=1
            print("El valor es: ", current_node.value)

    def update_node_value(self, index, new_value):
        search_node = self.get_node(index)
        if search_node != None:
            print(f"Actualizando el valor del nodo... \n >> {search_node.value} << por >> {new_value} << ")
            search_node.value = new_value
        else:
            print("No se encontró el el nodo")

    def remove_node(self, index):
        print(f"\n >>>>>> Eliminar nodo de la posicion {index} <<<<<<")
        if index == 1:
            self.shift_node_sll()
        elif index == self.length:
            self.delete_node_sll_pop()
        else:
            remove_node_sll = self.get_node(index)
            if remove_node_sll != None:
                previous_node = self.get_node(index - 1)
                print("Se va a eliminar: ",self.get_node(index).value)
                previous_node.next = remove_node_sll.next
                remove_node_sll.next = None
                self.length-=1
            else:
                print(" >>> No se encontró el nodo <<< ")
    
    def get_length(self):
        return self.length
    
    def search_index_node(self, node_value):
        if(self.length>0):
            current_node = self.head
            current_count = 1
            while node_value != current_node.value and current_count < self.length:
                current_node = current_node.next
                current_count+=1
            
            if current_count == self.length and node_value != current_node.value:
                print("No se encontró el indice del elemento buscado")
                return -1
            
            print("El índice del nodo con valor " + str(node_value) + " es: " + str(current_count))
            return current_count
            
        else:
            print("La lista está vacía")

    def reverse(self):
        if self.length > 1:
            aux_head = self.tail
            aux_tail = self.head
            if self.length == 2:
                self.head = aux_head
                self.head.next = aux_tail
                self.tail = aux_tail
                self.tail.next = None
                return
            
            current_node = self.tail
            for i in range (1, self.length - 1):
                node = self.get_node(self.length - i)
                current_node.next = node
                current_node = node
            node.next = aux_tail
            self.head = aux_head
            self.tail = aux_tail
            self.tail.next = None

    def delete_list(self):
        print(" >>> Eliminando todos los elementos de la lista <<< ")
        if self.head != None:
            self.head.next = None
            self.head = None
            self.tail = None
            self.length = 0

    def sort_list(self):
        array_with_nodes_value = list()
        current_node = self.head
        while(current_node != None):
            array_with_nodes_value.append(current_node.value)
            current_node = current_node.next
        #Imprimimos los valores de la lista
        sorted_list = sorted(array_with_nodes_value)
        print(f"Lista: {sorted_list}")
    
    
    def add_node(self, index, value):
        if self.length != self.max_length:
            print(f"\n >>>>>> Agregar nodo en la posición {index} <<<<<<")
            if index == 1:
                self.create_node_sll_unshift(value)
            elif index == self.length + 1:
                self.create_node_sll_ends(value)
            else:
                new_node = self.Node(value)
                actual_node_sll = self.get_node(index)
                if actual_node_sll != None:
                    previous_node = self.get_node(index - 1)
                    print("Se va a mover: ",actual_node_sll.value)
                    previous_node.next = new_node
                    new_node.next = actual_node_sll
                    self.length+=1
                else:
                    print(" >>> El índice no es accesible <<< ")
            return True
        return False


    def is_empty(self):
        if self.length == 0:
            print("Si está vacía")
            return True
        else:
            print("No está vacía")
            return False