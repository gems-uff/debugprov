from graphviz import Graph

from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.node import Node
from pyalgdb.validity import Validity

class Visualization:

    BUGGY_NODE_COLOR = 'red'
    PROVENANCE_COLOR = 'dodgerblue'
    INVALID_COLOR = 'darkorange1'
    VALID_COLOR = 'darkolivegreen1'
    #PROV_PRUNED_NODE = 'grey64'
    NODE_IN_EVALUATION = 'gold2'

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree

    def generate_exec_tree(self, graph_name = 'exec_tree'):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.ev_id), root_node.get_name(), fillcolor=self.INVALID_COLOR, style='filled') # root node
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.ev_id), str(eval_node.get_name()), fillcolor=self.NODE_IN_EVALUATION, style='filled')
        buggy_node = self.exec_tree.buggy_node
        if buggy_node is not None:
            self.graph.node(str(buggy_node.ev_id), str(buggy_node.get_name()), fillcolor=self.BUGGY_NODE_COLOR, style='filled')

    def view_exec_tree(self, graph_name = 'exec_tree'):
        self.generate_exec_tree(graph_name)
        self.graph.view()

    def view_exec_tree_prov(self, graph_name, dependencies:list):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        self.graph.attr('graph', ordering='out')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.ev_id), root_node.name, fillcolor=self.INVALID_COLOR, style='filled')
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.ev_id), str(eval_node.name), fillcolor=self.NODE_IN_EVALUATION, style='filled')
        for d in dependencies: # this loop draws the provenance links between nodes
            self.graph.edge(str(d.dependent.ev_id), str(d.influencer.ev_id), None, color=self.PROVENANCE_COLOR, dir='forward')
            self.graph.node(str(d.dependent.ev_id), None, fillcolor=self.PROVENANCE_COLOR, style='filled')
            self.graph.node(str(d.influencer.ev_id), None, fillcolor=self.PROVENANCE_COLOR, style='filled')
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
            # Uncomment this block below to paint not-in-provenance removed nodes with grey
            #if n.prov is None or n.prov is False:
            #    self.graph.node(str(n.ev_id), str(n.name), fillcolor=self.PROV_PRUNED_NODE, style='filled')
            #else:
            #    self.graph.node(str(n.ev_id), str(n.name))

        if len(chds) > 0:
            g = Graph()
            for c in chds:
                g.node(str(c.ev_id))
            g.graph_attr['rank']='same'
            self.graph.subgraph(g)

        for n in chds: 
            self.navigate(n)

    