import sys 
from node import Node


class ExecTreeCreator(): 

        QUERY = "select id, code_component_id, repr, name from evaluation natural join activation where activation_id = ?"

        def __init__(self):
                self.EXEC_TREE_ID = 0

        def get_root(self, cursor) -> Node:
                # root_query = "select * from activation where activation.id = 1"
                # safety: verify if one and only one root is found!
                for tupl in cursor.execute(self.QUERY, [0]):
                        return Node(tupl[0], tupl[1], tupl[2], tupl[3])

        def get_childrens_of_node(self, node, cursor):
                query = "select id, code_component_id, repr, name from evaluation natural join activation where activation_id = ?"
                childrens = []

                for tupl in cursor.execute(query, [node.id]):
                        # print("#")
                        # print(tupl)
                        # self.EXEC_TREE_ID = self.EXEC_TREE_ID + 1
                        childrens.append(Node(tupl[0], tupl[1], tupl[2], tupl[3]))

                for n in childrens:
                        chds = self.get_childrens_of_node(n, cursor)
                        n.childrens = chds

                return childrens    

        def create_exec_tree(self, cursor):
                print("Creating execution tree")
                print(cursor)
                root_node = self.get_root(cursor)
                print(root_node)
                root_node.childrens = self.get_childrens_of_node(root_node, cursor)
                return root_node
