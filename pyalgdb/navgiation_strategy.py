from node import Node

class NavigationStrategy:

    def navigate(self, exec_tree):
        raise NotImplementedError("Please Implement this method")


    def evaluate(self, node: Node) -> bool:
        print("-------------------------")
        print("Evaluating node {}".format(node.name))
        print("Name: {}".format(node.name))
        print("Evaluation_id: {}".format(node.id))
        print("Code_component_id: {}".format(node.code_component_id))
        print("Returns: {}".format(node.retrn))
        ans = input("Is correct? Y/N ")
        if ans == "Y" or ans == "y":
            return True
        else:
            return False