from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.validity import Validity
from pyalgdb.execution_tree import ExecutionTree

class DivideAndQuery(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def find_best_node(self, node:Node, w_2:float):
        if node.weight <= w_2:
            if (self.best_guess is None):
                self.best_guess = node
            elif node.weight > self.best_guess.weight:
                self.best_guess = node
        for c in node.childrens:
            if c.validity is Validity.UNKNOWN:
                self.find_best_node(c, w_2)

    def calculate_weights(self, node:Node):
        node.weight = self.weight(node)
        print(node.name+" "+str(node.weight))
        for c in node.childrens:
            self.calculate_weights(c)

    def weight(self, node: Node):
        chds = node.childrens
        summ = 0
        for c in chds:
            if c.validity == Validity.UNKNOWN:
                summ += 1 + self.weight(c)
        return summ

    def recursive_navigate(self, node: Node):
        self.calculate_weights(node)
        self.best_guess = None
        self.find_best_node(node, (node.weight/2))
        print("Best guess: {}".format(self.best_guess.name))
        print("Best guess weight: {}".format(str(self.best_guess.weight)))
        print("w/2: {}".format(node.weight/2))
        self.best_guess = self.evaluate(self.best_guess)
        if self.best_guess.validity is Validity.VALID:
            self.validate(self.best_guess)
            self.recursive_navigate(node)
        elif self.best_guess.validity is Validity.INVALID:
            for sibling in self.best_guess.parent.childrens:
                if sibling is not self.best_guess:
                    self.validate(sibling)
            self.recursive_navigate(self.best_guess)


    def validate(self, node):
        node.validity = Validity.VALID
        for c in node.childrens:
            self.validate(c)
            