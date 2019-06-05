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
            #invalid_nodes = [n for n in self.exec_tree.get_all_nodes() if n.validity is Validity.INVALID]
            #sorted_invalid_nodes = copy.deepcopy(invalid_nodes)
            #invalid_nodes.sort(key=lambda x: x.ev_id, reverse=True)
            #self.exec_tree.buggy_node = invalid_nodes[0]
            self.finish_navigation()
        else:
            return max(
                (n for n in self.exec_tree.get_all_nodes()
                if n.validity is Validity.UNKNOWN
                if n.weight <= w_2),
                key=lambda n: n.weight)
        #nodes = self.exec_tree.get_all_nodes()
        #best_guess = None
        #for n in nodes:
        #    if n.weight > best_guess and n.weight <= w_2 and n.validity == Validity.UNKOWN:
        #        best_guess = n
        #return n


   # def find_best_guess(self, node:Node, w_2:float):
   #     if node.weight <= w_2 and node.validity is Validity.UNKNOWN:
   #         if (self.best_guess is None):
   #             self.best_guess = node
   #         elif node.weight > self.best_guess.weight:
   #             self.best_guess = node
   #     for c in node.childrens:
   #         if c.validity is not Validity.VALID:
   #             self.find_best_guess(c, w_2)

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
            
            #if self.best_guess.validity is Validity.VALID:
            #    if self.best_guess.parent.has_childrens_with_validity(Validity.UNKNOWN):
            #        self.recursive_navigate(node)
            #    else:
            #        self.exec_tree.buggy_node = self.best_guess.parent
            #        self.finish_navigation()
            #    if self.best_guess.has_childrens_with_validity(Validity.UNKNOWN):
            #        print("IF")
            #        self.recursive_navigate(node)
            #    else:
            #        print("ELSE")
            #        self.exec_tree.buggy_node = self.best_guess
            #        self.finish_navigation()


            