from node import Node

class NavigationStrategy:

    def __init__(self, root_node: Node):
        self.root_node = root_node

    def navigate(self, exec_tree):
        raise NotImplementedError("Please Implement this method")

    def evaluate(self, node: Node) -> bool:
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
            return True
        else:
            return False