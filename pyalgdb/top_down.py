from navgiation_strategy import NavigationStrategy
from node import Node

class TopDown(NavigationStrategy):

    def navigate(self, exec_tree: Node):
        chds = exec_tree.childrens
        for node in chds:
            nd = self.evaluate(node)
            if (nd.validity is True):
                print("Nothing to do here, just go to next node.. ->>")
            else:
                if (nd.has_childrens()):
                    self.navigate(nd)
                else:
                    print("Finished navigation!")
                    return exec_tree
