from node import Node
from graphviz import Digraph

class Visualization:

    def __init__(self):
        self.graph = Digraph('exec_tree', filename='exec_tree.gv')
        self.graph.attr('node', shape='box')

    def view_exec_tree(self, exec_tree:Node):
        self.graph.node(str(exec_tree.id), exec_tree.name, fillcolor='red', style='filled')
        self.navigate(exec_tree)
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens
        for n in chds:
            self.graph.edge(str(node.id), str(n.id))
            if n.validity == False:
                self.graph.node(str(n.id), str(n.name), fillcolor='red', style='filled')
            else:
                self.graph.node(str(n.id), str(n.name), fillcolor='green', style='filled')
            self.navigate(n)

    