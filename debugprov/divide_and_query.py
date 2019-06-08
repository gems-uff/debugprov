from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity
from debugprov.execution_tree import ExecutionTree

class DivideAndQuery(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def find_best_guess(self,node,w_2):
        nodes_with_unknown_validity = [n for n in self.exec_tree.get_all_nodes() if n.validity is Validity.UNKNOWN]        
        if len(nodes_with_unknown_validity) == 0:
            self.finish_navigation()
        else:
            return max(
                (n for n in self.exec_tree.get_all_nodes()
                if n.validity is Validity.UNKNOWN
                if n.weight <= w_2),
                key=lambda n: n.weight)

    def weight(self, node: Node):
        summ = 0
        for c in node.childrens:
            if c.validity is Validity.UNKNOWN:
                summ += 1 + self.weight(c)
            else:
                summ += self.weight(c)
        node.weight = summ
        return summ

    def recursive_navigate(self, node: Node):
        self.weight(self.exec_tree.root_node)
        self.best_guess = None
        self.best_guess = self.find_best_guess(self.exec_tree.root_node, (self.exec_tree.root_node.weight/2))
        print("Best guess: {}".format(self.best_guess))
        if self.best_guess is not None:
            self.evaluate(self.best_guess)
            if self.best_guess.validity is Validity.INVALID:
                p = self.best_guess.parent
                while p is not None:
                    p.validity = Validity.INVALID
                    p = p.parent
            self.recursive_navigate(node)
                        