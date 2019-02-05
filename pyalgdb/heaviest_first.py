from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.validity import Validity

class HeaviestFirst(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        self.weight(node)
        # sort by weight, from bigger to smaller
        node.childrens.sort(key=lambda x: x.weight, reverse=True)
        for n in node.childrens:
            if self.exec_tree.buggy_node is None:
                if n.validity == Validity.UNKNOWN:
                    self.evaluate(n)
                    if n.validity is Validity.VALID:
                        self.recursive_validate(n)
                        if n.parent.all_childrens_are_valid():
                            self.exec_tree.buggy_node = n.parent
                            self.finish_navigation()
                    if n.validity == Validity.INVALID:
                        for j in node.childrens:
                            if j is not n:
                                self.recursive_validate(j)
                        if n.has_childrens_with_validity(Validity.UNKNOWN):
                            self.recursive_navigate(n)
                        else:
                            self.exec_tree.buggy_node = n
                            self.finish_navigation()


    def weight(self, node: Node):
        summ = 0
        for c in node.childrens:
            summ += 1 + self.weight(c)
        node.weight = summ
        return summ