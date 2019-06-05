from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity

class TopDown(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        for n in node.childrens:
            if self.exec_tree.buggy_node is None:
                if n.validity == Validity.UNKNOWN:
                    self.evaluate(n)
                elif n.validity == Validity.NOT_IN_PROV:
                    # workaround to ignore nodes that are not in the
                    # provenance dag, but without removing its childs
                    # (the childs can be in the dag)
                    if n.has_childrens():
                        self.recursive_navigate(n)     
                if n.validity == Validity.INVALID:
                    self.recursive_validate(self.exec_tree.root_node,n)
                    if n.has_childrens_with_validity(Validity.UNKNOWN):
                        self.recursive_navigate(n)
                    else:
                        self.exec_tree.buggy_node = n
                        self.finish_navigation()
                if n.validity == Validity.VALID:
                    print("if n.validity == Validity.VALID:")
                    siblings = [j for j in n.parent.childrens if j.validity is Validity.UNKNOWN]
                    if len(siblings) == 0:
                        self.exec_tree.buggy_node = n.parent
                        self.finish_navigation()

                    #if n.parent.all_childrens_are_valid():
                    #elif not n.parent.has_childrens_with_validity(Validity.UNKNOWN):
                    #    self.exec_tree.buggy_node = n
                    #    self.finish_navigation()
                    
