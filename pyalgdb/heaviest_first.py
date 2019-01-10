from navgiation_strategy import NavigationStrategy
from node import Node

class HeaviestFirst(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.root_node)
        return self.root_node

    def recursive_navigate(self, node: Node):
        chds = node.childrens
        for n in chds:
            n.weight = self.weight(n)
            
        # sort by weight, from bigger to smaller
        chds.sort(key=lambda x: x.weight, reverse=True)

        for n in chds:
            if n.validity is None:
                n.validity = self.evaluate(n)
            if (n.validity is False):
                for j in chds:
                    if j.validity is None:
                        j.validity = True
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