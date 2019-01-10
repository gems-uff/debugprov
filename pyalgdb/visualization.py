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

    def view_exec_tree_prov(self, exec_tree:Node, dependencies:list):
        self.graph.node(str(exec_tree.id), exec_tree.name, fillcolor='red', style='filled')
        self.navigate(exec_tree)
        for d in dependencies:
            if d.source.typeof != 'STARTER':
                source_node = self.search_for_node(d.source.id, exec_tree)[0] #gambiarra feia pra cacete, corrigir!
                target_node = self.search_for_node(d.target.id, exec_tree)[0]
                #print(source_node + ' -> ' + target_node)
                if source_node is not None and target_node is not None:
                    self.graph.edge(str(source_node.id), str(target_node.id), None, color='magenta2')
        self.graph.view()

    # problema: podem existir diversos nós com o mesmo code_component_id
    def search_for_node(self, id, node:Node):
        nodes = []
        if node.code_component_id == id:
            nodes.append(node)
        for c in node.childrens:
            nodes.extend(self.search_for_node(id, c))
        return nodes

    def navigate(self, node:Node):
        chds = node.childrens
        s = Digraph('subgraph_'+str(node.id))
        s.graph_attr.update(rank='subgraph_'+str(node.name))
        for n in chds:
            s.edge(str(node.id), str(n.id))
            if n.validity == False:
                s.node(str(n.id), str(n.name), fillcolor='red', style='filled')
            else:
                s.node(str(n.id), str(n.name), fillcolor='green', style='filled')
            self.navigate(n)
        self.graph.subgraph(s)

    