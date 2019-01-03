class Node:
    
    def __init__(self, id, name, activation_id):
        self.id = id
        self.name = name
        self.activation_id = activation_id
        self.childrens = []