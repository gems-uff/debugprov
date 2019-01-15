from navgiation_strategy import NavigationStrategy
from node import Node
from validity import Validity

class SingleStepping(NavigationStrategy):
    
    def navigate(self):
        self.found = False
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree


    def recursive_navigate(self, node: Node):
        if node.has_childrens():
            for c in node.childrens:
                    self.recursive_navigate(c)
        if self.found is False:
            node = self.evaluate(node)
            if node.validity is Validity.INVALID:
                self.found = True
