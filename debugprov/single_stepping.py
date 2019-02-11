from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity

class SingleStepping(NavigationStrategy):
    
    def navigate(self):
        self.found = False
        self.recursive_navigate(self.exec_tree.root_node)
        self.finish_navigation()
        return self.exec_tree

    def recursive_navigate(self, current_node: Node):
        if current_node.has_childrens():
            for c in current_node.childrens:
                self.recursive_navigate(c)
        if self.found is False:
            self.evaluate(current_node)            
            if current_node.validity is Validity.INVALID:
                self.exec_tree.buggy_node = current_node
                self.found = True