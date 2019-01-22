from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.validity import Validity

class TopDown(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        for n in node.childrens:
            if n.validity == Validity.UNKNOWN:
                self.evaluate(n)
            if n.validity == Validity.INVALID:
                for j in node.childrens:
                    if j.validity == Validity.UNKNOWN:
                        self.recursive_validate(j)
                if (n.has_childrens()):
                    self.recursive_navigate(n)
                    