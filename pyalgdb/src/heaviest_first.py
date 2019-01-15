from src.navgiation_strategy import NavigationStrategy
from src.node import Node
from src.validity import Validity

class HeaviestFirst(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        chds = node.childrens
        for n in chds:
            n.weight = self.weight(n)
        # sort by weight, from bigger to smaller
        chds.sort(key=lambda x: x.weight, reverse=True)
        for n in chds:
            if n.validity == Validity.UNKNOWN:
                n = self.evaluate(n)
            if (n.validity == Validity.INVALID):
                for j in chds:
                    if j.validity == Validity.UNKNOWN:
                        j.validity = Validity.VALID
                if (n.has_childrens()):
                    self.recursive_navigate(n)

    def weight(self, node: Node):
        if not node.has_childrens():
            return 0
        else:
            chds = node.childrens
            summ = 0
            for c in chds:
                summ += 1 + self.weight(c)
            return summ