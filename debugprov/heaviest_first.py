import copy
from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity

class HeaviestFirst(NavigationStrategy):

    def navigate(self):
        self.evaluate(self.exec_tree.root_node)
        if self.exec_tree.root_node.validity is Validity.VALID:
            print("ERROR")
            import sys
            sys.exit(1)
        else:
            self.recursive_navigate(self.exec_tree.root_node)
            return self.exec_tree

    def recursive_navigate(self, node: Node):
        self.weight(node)
        # sort by weight, from bigger to smaller
        sorted_childrens = copy.deepcopy(node.childrens)
        sorted_childrens.sort(key=lambda x: x.weight, reverse=True)
        #node.childrens.sort(key=lambda x: x.weight, reverse=True)
        for srtd_n in sorted_childrens:
            if self.exec_tree.buggy_node is None:
                n = self.exec_tree.search_by_ev_id(srtd_n.ev_id)
                if n.validity == Validity.UNKNOWN:
                    self.evaluate(n)
                elif n.validity == Validity.NOT_IN_PROV:
                    # workaround to ignore nodes that are not in the
                    # provenance dag, but without removing its childs
                    # (the childs can be in the dag)
                    if n.has_childrens():
                        self.recursive_navigate(n)      
                if n.validity is Validity.VALID:
                    self.recursive_validate(n)
                    if n.parent.all_childrens_are_valid():
                        self.exec_tree.buggy_node = n.parent
                        self.finish_navigation()
                    elif not n.parent.has_childrens_with_validity(Validity.UNKNOWN):
                        self.exec_tree.buggy_node = n.parent
                        self.finish_navigation()
					
                if n.validity == Validity.INVALID:
                    self.recursive_validate(self.exec_tree.root_node,n)
                    #for j in node.childrens:
                    #    if j is not n:
                    #        self.recursive_validate(j)
                    if n.has_childrens_with_validity(Validity.UNKNOWN):
                        self.recursive_navigate(n)
                    else:
                        self.exec_tree.buggy_node = n
                        self.finish_navigation()

    def weight(self, node: Node):
        summ = 0
        for c in node.childrens:
            if c.validity is Validity.NOT_IN_PROV:
                summ += self.weight(c)
            else:
                summ += 1 + self.weight(c)
        node.weight = summ
        return summ