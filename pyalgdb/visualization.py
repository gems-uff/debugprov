from graphviz import Graph

from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.node import Node
from pyalgdb.validity import Validity

class Visualization:

    PROVENANCE_COLOR = 'magenta2'
    PROV_PRUNED_NODE = 'grey64'

    NODE_IN_EVALUATION = 'cyan1'

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree

    def generate_exec_tree(self, graph_name = 'exec_tree'):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.id), root_node.name) # root node
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.id), str(eval_node.name), fillcolor=self.NODE_IN_EVALUATION, style='filled')

    def view_exec_tree(self, graph_name = 'exec_tree'):
        self.generate_exec_tree(graph_name)
        self.graph.view()

    def view_exec_tree_prov(self, graph_name, dependencies:list):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.id), root_node.name)
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.id), str(eval_node.name), fillcolor=self.NODE_IN_EVALUATION, style='filled')
        for d in dependencies: # this loop draws the provenance links between nodes
            source_nodes = self.exec_tree.search_for_node_by_ccid(d.source.id)
            target_nodes = self.exec_tree.search_for_node_by_ccid(d.target.id)
            for sn in source_nodes:
                for tn in target_nodes:
                    self.graph.edge(str(sn.id), str(tn.id), None, color=self.PROVENANCE_COLOR, dir='forward')
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens

        for n in chds:
            self.graph.edge(str(node.id), str(n.id), None, dir='forward')
            if n.validity == Validity.INVALID:
                self.graph.node(str(n.id), str(n.name), fillcolor='red', style='filled')
            elif n.validity == Validity.VALID: 
                self.graph.node(str(n.id), str(n.name), fillcolor='green', style='filled')
            elif n.validity == Validity.UNKNOWN:  
                self.graph.node(str(n.id), str(n.name))
            # Uncomment this block below to paint not-in-provenance removed nodes with grey
            #    if n.prov is None or n.prov is False:
            #        self.graph.node(str(n.id), str(n.name), fillcolor=self.PROV_PRUNED_NODE, style='filled')
            #    else:
            #        self.graph.node(str(n.id), str(n.name))

        if len(chds) > 0:
            g = Graph()
            for c in chds:
                g.node(str(c.id))
            g.graph_attr['rank']='same'
            self.graph.subgraph(g)

        for n in chds: 
            self.navigate(n)

    