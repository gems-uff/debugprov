from graphviz import Graph

from debugprov.execution_tree import ExecutionTree
from debugprov.node import Node
from debugprov.validity import Validity

class Visualization:

    BUGGY_NODE_COLOR = 'red'
    PROVENANCE_EDGE_COLOR = 'dodgerblue'
    INVALID_COLOR = 'darkorange1'
    VALID_COLOR = 'darkolivegreen1'
    NODE_IN_EVALUATION_COLOR = 'gold2'
    PROV_PRUNED_NODE_COLOR = 'grey55'

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree

    def generate_exec_tree(self, graph_name = 'exec_tree'):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        self.graph.attr('graph', ordering='out')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.ev_id), root_node.get_name(), fillcolor=self.INVALID_COLOR, style='filled') # root node
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.ev_id), str(eval_node.get_name()), fillcolor=self.NODE_IN_EVALUATION_COLOR, style='filled')
        buggy_node = self.exec_tree.buggy_node
        if buggy_node is not None:
            self.graph.node(str(buggy_node.ev_id), str(buggy_node.get_name()), fillcolor=self.BUGGY_NODE_COLOR, style='filled')
        #if self.exec_tree.dependencies is not None:
        #    for d in self.exec_tree.dependencies:
        #        self.graph.edge(str(d.source.ev_id), str(d.target.ev_id), None, color=self.PROVENANCE_EDGE_COLOR, dir='forward')

    def view_exec_tree(self, graph_name = 'exec_tree'):
        self.generate_exec_tree(graph_name)
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens
        for n in chds:
            self.graph.edge(str(node.ev_id), str(n.ev_id), None, dir='forward')
            if n.validity == Validity.INVALID:
                self.graph.node(str(n.ev_id), str(n.get_name()), fillcolor=self.INVALID_COLOR, style='filled')
            elif n.validity == Validity.VALID: 
                self.graph.node(str(n.ev_id), str(n.get_name()), fillcolor=self.VALID_COLOR, style='filled')
            elif n.validity == Validity.UNKNOWN:  
                self.graph.node(str(n.ev_id), str(n.get_name()))
            elif n.validity is Validity.NOT_IN_PROV:
                self.graph.node(str(n.ev_id), str(n.get_name()), fillcolor=self.PROV_PRUNED_NODE_COLOR, style='filled')
                
        if len(chds) > 0:
            g = Graph()
            for c in chds:
                g.node(str(c.ev_id))
            g.graph_attr['rank']='same'
            self.graph.subgraph(g)

        for n in chds: 
            self.navigate(n)

    