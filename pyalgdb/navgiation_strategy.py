from pyalgdb.node import Node
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.validity import Validity

class NavigationStrategy:

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree

    def navigate(self)->ExecutionTree:
        raise NotImplementedError("Abstract method: Please Implement this method in subclass")

    def evaluate(self, node: Node) -> Node:
        print("-------------------------")
        print("Evaluating node {}".format(node.name))
        print("Name: {}".format(node.name))
        print("Evaluation_id: {}".format(node.id))
        print("Code_component_id: {}".format(node.code_component_id))
        print("Parameters: name | value ")
        for p in node.params:
            print (" {} | {} ".format(p.name, p.value))
        print("Returns: {}".format(node.retrn))
        ans = input("Is correct? Y/N ")
        if ans == "Y" or ans == "y":
            node.validity = Validity.VALID
        else:
            node.validity = Validity.INVALID
        return node