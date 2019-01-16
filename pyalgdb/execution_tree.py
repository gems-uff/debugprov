from pyalgdb.node import Node

class ExecutionTree:

    def __init__(self, root_node:Node):
        self.root_node = root_node

    def search_for_node_by_ccid(self, code_component_id):
        return self.recursive_search_for_node_ccid(code_component_id, self.root_node)

    def recursive_search_for_node_ccid(self, code_component_id, node:Node):
        nodes = []
        if node.code_component_id == code_component_id:
            nodes.append(node)
        for c in node.childrens:
            nodes.extend(self.recursive_search_for_node_ccid(code_component_id, c))
        return nodes