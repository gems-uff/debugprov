from debugprov.node import Node
from debugprov.execution_tree import ExecutionTree

class ExecTreeCreator(): 

        def __init__(self, cursor):
                self.cursor = cursor
                self.query = ("select EV.id, CC.id, EV.repr, CC.name "
                              "from evaluation EV "
                              "natural join activation ACT "
                              "join code_component CC on EV.code_component_id = CC.id "
                              "where activation_id = ? ")

        def create_exec_tree(self):
                root_node = self.get_root()
                root_node.childrens = self.get_childrens_of_node(root_node)
                self.get_params(root_node)
                return ExecutionTree(root_node)

        def get_root(self) -> Node:
                self.cursor.execute(self.query, [0])
                result = self.cursor.fetchall()
                if len(result) != 1:
                        raise ValueError("ValueError: Something wrong in database. {} root nodes found".format(len(result)))

                for tupl in self.cursor.execute(self.query, [0]):
                        root = Node(tupl[0], tupl[1], tupl[2], tupl[3], None)
                        return root

        def get_childrens_of_node(self, node):
                childrens = []
                for tupl in self.cursor.execute(self.query, [node.ev_id]):
                        n = Node(tupl[0], tupl[1], tupl[2], tupl[3], node)
                        childrens.append(n)
                for n in childrens:
                        chds = self.get_childrens_of_node(n)
                        n.childrens = chds
                return childrens    


        def get_params(self, node:Node):
                for chd in node.childrens:
                        chd.get_parameters(self.cursor)
                        self.get_params(chd)