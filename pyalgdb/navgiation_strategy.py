class NavigationStrategy:

    def navigate(self, exec_tree):
        raise NotImplementedError("Please Implement this method")


    def evaluate(self, node):
        print("Evaluating node")
        print(node.name)
        ans = input("Is correct? Y/N ")
        if ans == "Y":
            node.validity = True
        else:
            node.validity = False
        return node