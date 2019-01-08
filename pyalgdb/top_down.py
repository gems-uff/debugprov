from navgiation_strategy import NavigationStrategy
from node import Node

class TopDown(NavigationStrategy):

    def navigate(self, exec_tree: Node):
        chds = exec_tree.childrens
        for node in chds:
            result = self.evaluate(node)
            node.validity = result
            if (node.validity is True):
                print("Nothing to do here, just go to next node.. ->>")
            else:
                if (node.has_childrens()):
                    self.navigate(node)
                else:
                    print("Finished navigation!")
                    return exec_tree
