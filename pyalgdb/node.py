class Node:
    
    def __init__(self, id, code_component_id, retrn, name):
        self.id = id
        self.code_component_id = code_component_id
        self.retrn = retrn
        self.name = name
        self.childrens = []

    def has_childrens(self):
        return len(self.childrens) > 0