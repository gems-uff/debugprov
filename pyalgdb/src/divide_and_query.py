from navgiation_strategy import NavigationStrategy
from node import Node
from validity import Validity
from execution_tree import ExecutionTree

class DivideAndQuery(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def find_best_node(self, node:Node, w_2:float):
        if node.weight > self.best_guess.weight and node.weight <= w_2:
            self.best_guess = node
        for c in node.childrens:
            self.find_best_node(c, w_2)

    def calculate_weights(self, node:Node):
        node.weight = self.weight(node)
        for c in node.childrens:
            self.calculate_weights(c)

    def weight(self, node: Node):
        if not node.has_childrens():
            return 0
        else:
            chds = node.childrens
            summ = 0
            for c in chds:
                summ += 1 + self.weight(c)
            return summ

    def recursive_navigate(self, node: Node):
        self.calculate_weights(node)
        self.best_guess = Node("", "", "", "", None)
        self.best_guess.weight = 0
        self.find_best_node(node, (node.weight/2))
        print("Best guess: {}".format(self.best_guess.name))
        print("Best guess weight: {}".format(str(self.best_guess.weight)))
        print("w/2: {}".format(node.weight/2))
        self.best_guess = self.evaluate(self.best_guess)
        if self.best_guess.validity is Validity.VALID:
            bg = self.best_guess
            self.best_guess.parent.childrens.remove(bg)
            self.recursive_navigate(node)
        elif self.best_guess.validity is Validity.INVALID:
            for sibling in self.best_guess.parent.childrens:
                if sibling is not self.best_guess:
                    self.best_guess.parent.childrens.remove(sibling)
            