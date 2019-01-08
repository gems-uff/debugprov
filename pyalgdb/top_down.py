from navgiation_strategy import NavigationStrategy
from node import Node

class TopDown(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.root_node)
        return self.root_node


    def recursive_navigate(self, node: Node):
        chds = node.childrens
        for n in chds:
            if n.validity is None:
                n.validity = self.evaluate(n)
            if (n.validity is False):
                for j in chds:
                    if j.validity == None:
                        j.validity = True
                if (n.has_childrens()):
                    self.recursive_navigate(n)