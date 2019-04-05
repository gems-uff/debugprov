from debugprov.node import Node

class ExecutionTree:

    def __init__(self, root_node:Node):
        self.root_node = root_node
        self.buggy_node = None
        self.node_under_evaluation = None
        self.is_prov_enhanced = False
        self.dependencies = None

    def search_by_ccid(self, code_component_id):
        return self.recursive_search_by_ccid(code_component_id, self.root_node)

    def recursive_search_by_ccid(self, code_component_id, node:Node):
        nodes = []
        if node.code_component_id == code_component_id:
            nodes.append(node)
        for c in node.childrens:
            nodes.extend(self.recursive_search_by_ccid(code_component_id, c))
        return nodes

    def search_by_ev_id(self, ev_id):
        all_nodes = self.get_all_nodes()
        for n in all_nodes:
            if n.ev_id == ev_id:
                return n

    def get_all_nodes(self):
        return self._get_all_nodes(self.root_node)

    def _get_all_nodes(self, node):
        nodes = []
        nodes.append(node)
        if node.childrens is not None and len(node.childrens) > 0:
            for c in node.childrens:
                nodes.extend(self._get_all_nodes(c))
        return nodes