from node import Node
from tree_helper import TreeHelper
from graphviz import Graph

class Visualization:

    PROVENANCE_COLOR = 'magenta2'

    def __init__(self):
        self.graph = Graph('exec_tree', filename='exec_tree.gv')
        self.graph.attr('node', shape='box')

    def view_exec_tree(self, exec_tree:Node):
        self.graph.node(str(exec_tree.id), exec_tree.name, fillcolor='red', style='filled')
        self.navigate(exec_tree)
        self.graph.view()

    def view_exec_tree_prov(self, exec_tree:Node, dependencies:list):
        self.graph.node(str(exec_tree.id), exec_tree.name, fillcolor='red', style='filled')
        self.navigate(exec_tree)
        tree_helper = TreeHelper(exec_tree)
        for d in dependencies:
            if d.source.typeof == 'STARTER':
                self.graph.node(str(d.source.id), d.source.name, shape='none', color=self.PROVENANCE_COLOR)
                target_nodes = tree_helper.search_for_node(d.target.id)
                for tn in target_nodes:
                    self.graph.edge(str(d.source.id), str(tn.id), None, color=self.PROVENANCE_COLOR)
            else:
                source_nodes = tree_helper.search_for_node(d.source.id)
                target_nodes = tree_helper.search_for_node(d.target.id)
                for sn in source_nodes:
                    for tn in target_nodes:
                        self.graph.edge(str(sn.id), str(tn.id), None, color=self.PROVENANCE_COLOR)
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens
        #rank = "same; "
        #for c in chds:
        #    rank = rank + "{}; ".format(c.id)

        #self.graph.attr(rank="{}".format(rank))

        for n in chds:
            self.graph.edge(str(node.id), str(n.id))
            if n.validity == False: # invalid node
                self.graph.node(str(n.id), str(n.name), fillcolor='red', style='filled')
            elif n.validity == True: # valid node
                self.graph.node(str(n.id), str(n.name), fillcolor='green', style='filled')
            else:  # node with unknown validity
                self.graph.node(str(n.id), str(n.name))
#        self.graph.subgraph(s)

        g = Graph()
        for c in chds:
            g.node(str(c.id))
        g.graph_attr['rank']='same'

        self.graph.subgraph(g)

        for n in chds: 
            self.navigate(n)

    