from pyalgdb.node import Node
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.validity import Validity
from pyalgdb.visualization import Visualization
from pyalgdb.answer_reader import AnswerReader
from pyalgdb.navigation_logger import NavigationLogger

class NavigationStrategy:

    def __init__(self, exec_tree: ExecutionTree, automated = False, answer_file = None):
        self.exec_tree = exec_tree
        self.AUTOMATED_NAVIGATION = automated
        if self.AUTOMATED_NAVIGATION:
            answer_reader = AnswerReader(answer_file)
            self.answers = answer_reader.read_answers()
            self.nav_log = NavigationLogger()
            self.nav_log.log("Navigation Strategy: {}".format(self.__class__.__name__))
            self.sequence_num = 0

    def navigate(self)->ExecutionTree:
        raise NotImplementedError("Abstract method: Please Implement this method in subclass")

    def evaluate(self, node: Node) -> Node:
        if self.AUTOMATED_NAVIGATION:
            self._automated_evaluation(node)
        else:
            self._interactive_evaluation(node)
    
    def _automated_evaluation(self, node:Node) -> Node:
        self.sequence_num += 1
        seq_num = " {} ".format(str(self.sequence_num))
        self.exec_tree.node_under_evaluation = node
        self.nav_log.log_node(node, self.sequence_num)
        if self.answers[node.id] is Validity.VALID:
            # The YES answer prunes the subtree rooted at N
            self.recursive_validate(node)
            self.nav_log.log(seq_num+"The node was defined as VALID")
        elif self.answers[node.id] is Validity.INVALID:
            # The NO answer prunes all the nodes of the ET,
            # exept the subtree rooted at N
            node.validity = Validity.INVALID
            if node.parent is not None:
                for c in node.parent.childrens:
                    if c is not node:
                        self.recursive_validate(c)
            self.nav_log.log(seq_num+"The node was defined as INVALID")
        self.exec_tree.node_under_evaluation = None
        return node

    def _interactive_evaluation(self, node: Node) -> Node:
        self.exec_tree.node_under_evaluation = node
        vis = Visualization(self.exec_tree)
        vis.view_exec_tree(str(id(node)))
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
            # The YES answer prunes the subtree rooted at N
            self.recursive_validate(node)
        else:
            # The NO answer prunes all the nodes of the ET,
            # exept the subtree rooted at N
            node.validity = Validity.INVALID
            if node.parent is not None:
                for c in node.parent.childrens:
                    if c is not node:
                        self.recursive_validate(c)

        self.exec_tree.node_under_evaluation = None
        return node


    def recursive_validate(self, node):
        node.validity = Validity.VALID
        for c in node.childrens:
            self.recursive_validate(c)

