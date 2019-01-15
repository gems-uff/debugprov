from navgiation_strategy import NavigationStrategy
from node import Node
from validity import Validity

class TopDown(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree


    def recursive_navigate(self, node: Node):
        chds = node.childrens
        for n in chds:
            if n.validity == Validity.UNKNOWN:
                n = self.evaluate(n)
            if n.validity == Validity.INVALID:
                for j in chds:
                    if j.validity == Validity.UNKNOWN:
                        j.validity = Validity.VALID
                if (n.has_childrens()):
                    self.recursive_navigate(n)