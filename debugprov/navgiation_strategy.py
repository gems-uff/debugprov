from debugprov.console_evaluation import ConsoleEvaluation
from debugprov.node import Node
from debugprov.execution_tree import ExecutionTree
from debugprov.validity import Validity
from debugprov.visualization import Visualization
from debugprov.answer_reader import AnswerReader
from debugprov.navigation_logger import NavigationLogger

class NavigationStrategy:

    def __init__(self, exec_tree: ExecutionTree, automated = False, answer_file = None):
        self.exec_tree = exec_tree
        self.AUTOMATED_NAVIGATION = automated
        if self.AUTOMATED_NAVIGATION:
            answer_reader = AnswerReader(answer_file)
            data = answer_reader.read_answers()
            self.invalid_nodes = data['invalid_nodes']
            self.wrong_node_id = data['node_with_wrong_data_id']
            #self.nav_log = NavigationLogger()
            #self.nav_log.log("Navigation Strategy: {}".format(self.__class__.__name__))
            self.sequence_num = 0

    def navigate(self)->ExecutionTree:
        raise NotImplementedError("Abstract method: Please Implement this method in subclass")

    def evaluate(self, node: Node) -> Node:
        if node.validity is Validity.UNKNOWN:
            if self.AUTOMATED_NAVIGATION:
                self._automated_evaluation(node)
            else:
                self._interactive_evaluation(node)
    
    def _automated_evaluation(self, node:Node) -> Node:
        self.sequence_num += 1
        seq_num = " {} ".format(str(self.sequence_num))
        self.exec_tree.node_under_evaluation = node
        #self.nav_log.log_node(node, self.sequence_num)
        if node.ev_id not in self.invalid_nodes:
            # The YES answer prunes the subtree rooted at N
            self.recursive_validate(node)
            #self.nav_log.log(seq_num+"The node was defined as VALID")
        elif node.ev_id in self.invalid_nodes:
            print(node.ev_id)
            # The NO answer prunes all the nodes of the ET,
            # exept the subtree rooted at N
            node.validity = Validity.INVALID
            self.recursive_validate(self.exec_tree.root_node,node)
            #if node.parent is not None:
            #    for c in node.parent.childrens:
            #        if c is not node:
            #            self.recursive_validate(c)
          #  self.nav_log.log(seq_num+"The node was defined as INVALID")
        self.exec_tree.node_under_evaluation = None
        return node

    def _interactive_evaluation(self, node: Node) -> Node:
        self.exec_tree.node_under_evaluation = node
        vis = Visualization(self.exec_tree)
        vis.view_exec_tree(str(id(node)))
        answer = ConsoleEvaluation.evaluate_node(node)
        if answer:
            # The YES answer prunes the subtree rooted at N
            self.recursive_validate(node)
        else:
            # The NO answer prunes all the nodes of the ET,
            # exept the subtree rooted at N
            node.validity = Validity.INVALID
            self.recursive_validate(self.exec_tree.root_node,node)
            #if node.parent is not None:
            #    for c in node.parent.childrens:
            #        if c is not node:
            #            self.recursive_validate(c)
        self.exec_tree.node_under_evaluation = None
        return node

    def recursive_validate(self, node, forbidden=None):
        print("RECURSIVE VALIDATE {}".format(node.ev_id))
        if node is forbidden:
            return
        # if node.validity is not Validity.NOT_IN_PROV:
        if node.validity is Validity.UNKNOWN:
            node.validity = Validity.VALID
        for c in node.childrens:
            self.recursive_validate(c,forbidden)

    def there_are_nodes_with_unknown_validity(self):
        nodes_with_unknown_validity = [n for n in self.exec_tree.get_all_nodes() if n.validity is Validity.UNKNOWN]        
        if len(nodes_with_unknown_validity) > 0:
            return True
        else:
            return False
    
    def finish_navigation(self):
        if self.exec_tree.buggy_node is None:
            invalid_nodes = [n.ev_id for n in self.exec_tree.get_all_nodes() if n.validity is Validity.INVALID]        
            #print("invalid nodes: {}".format(invalid_nodes))
            if len(invalid_nodes) == 0:
                not_in_prov_nodes = [n for n in self.exec_tree.get_all_nodes() if n.validity is Validity.NOT_IN_PROV]
                if len(not_in_prov_nodes) == 0: 
                    self.exec_tree.buggy_node = Node('inf','inf','inf','inf','inf')
                else:
                    print("The buggy node was not found in the provenance")
                    print("Searching in the remaining nodes")
                    for n in not_in_prov_nodes:
                        n.validity = Validity.UNKNOWN
                    self.navigate()
            else:
                self.exec_tree.buggy_node = self.exec_tree.search_by_ev_id(max(invalid_nodes))