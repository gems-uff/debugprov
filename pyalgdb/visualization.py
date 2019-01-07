from node import Node
from graphviz import Digraph

class Visualization:

    def __init__(self):
        self.graph = Digraph('exec_tree', filename='exec_tree.gv')

    def view_exec_tree(self, exec_tree:Node):
        self.graph.node(exec_tree.name)
        self.navigate(exec_tree)
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens
        for n in chds:
            self.graph.edge(node.name, n.name)
            self.navigate(n)