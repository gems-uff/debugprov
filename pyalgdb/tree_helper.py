from node import Node

class TreeHelper:

    def __init__(self, exec_tree: Node):
        self.exec_tree = exec_tree

    def search_for_node(self, code_component_id):
        return self.recursive_search_for_node(code_component_id, self.exec_tree)

    def recursive_search_for_node(self, code_component_id, node:Node):
        nodes = []
        if node.code_component_id == code_component_id:
            nodes.append(node)
        for c in node.childrens:
            nodes.extend(self.recursive_search_for_node(code_component_id, c))
        return nodes
