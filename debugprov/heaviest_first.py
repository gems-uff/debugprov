import copy
from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity

class HeaviestFirst(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        if self.there_are_nodes_with_unknown_validity():
            self.weight(node)
            self.evaluate(node)
            if node.validity is Validity.INVALID:
                # sort by weight, from bigger to smaller
                sorted_childrens = copy.deepcopy(node.childrens)
                sorted_childrens.sort(key=lambda x: x.weight, reverse=True)
                for srtd_n in sorted_childrens:
                    n = self.exec_tree.search_by_ev_id(srtd_n.ev_id)
                    self.recursive_navigate(n)

    def weight(self, node: Node):
        summ = 0
        for c in node.childrens:
            if c.validity is Validity.UNKNOWN:
                summ += 1 + self.weight(c)
            else:
                summ += self.weight(c)
        node.weight = summ
        return summ