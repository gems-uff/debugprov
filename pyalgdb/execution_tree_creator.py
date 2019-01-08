import sys 
from node import Node


class ExecTreeCreator(): 

        def __init__(self, cursor):
                self.cursor = cursor
                self.query = ("select EV.id, CC.id, EV.repr, CC.name "
                              "from evaluation EV "
                              "natural join activation ACT "
                              "join code_component CC on EV.code_component_id = CC.id "
                              "where activation_id = ? ")

        def get_root(self) -> Node:
                # root_query = "select * from activation where activation.id = 1"
                # safety: verify if one and only one root is found!
                for tupl in self.cursor.execute(self.query, [0]):
                        return Node(tupl[0], tupl[1], tupl[2], tupl[3])

        def get_childrens_of_node(self, node):
                # query = "select id, code_component_id, repr, name from evaluation natural join activation where activation_id = ?"
                childrens = []

                for tupl in self.cursor.execute(self.query, [node.id]):
                        n = Node(tupl[0], tupl[1], tupl[2], tupl[3])
                        childrens.append(n)

                for n in childrens:
                        chds = self.get_childrens_of_node(n)
                        n.childrens = chds

                return childrens    

        def create_exec_tree(self):
                root_node = self.get_root()
                root_node.childrens = self.get_childrens_of_node(root_node)
                self.get_params(root_node)
                return root_node

        def get_params(self, node:Node):
                for chd in node.childrens:
                        chd.get_parameters(self.cursor)
                        self.get_params(chd)