from pyalgdb.node import Node
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.validity import Validity
from pyalgdb.visualization import Visualization

class NavigationStrategy:

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree

    def navigate(self)->ExecutionTree:
        raise NotImplementedError("Abstract method: Please Implement this method in subclass")

    def evaluate(self, node: Node) -> Node:
        self.exec_tree.node_under_evaluation = node
        vis = Visualization(self.exec_tree)
        vis.view_exec_tree(str(id(node)))
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
            # The YES answer prunes the subtree rooted at N
            self.recursive_validate(node)
        else:
            # The NO answer prunes all the nodes of the ET,
            # exept the subtree rooted at N
            node.validity = Validity.INVALID
            if node.parent is not None:
                for c in node.parent.childrens:
                    if c is not node:
                        self.recursive_validate(c)

        self.exec_tree.node_under_evaluation = None
        return node


    def recursive_validate(self, node):
        node.validity = Validity.VALID
        for c in node.childrens:
            self.recursive_validate(c)

