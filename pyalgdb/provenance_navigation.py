from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.code_component import CodeComponent
from pyalgdb.dependency_rel import DependencyRel
from pyalgdb.validity import Validity
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.visualization import Visualization
from pyalgdb.provenance_tools import ProvenanceTools

class ProvenanceNavigation(NavigationStrategy):

    def __init__(self, exec_tree: ExecutionTree, cursor):
        super().__init__(exec_tree)
        self.prov_tools = ProvenanceTools(cursor)
        self.cursor = cursor
        self.VISITED_CCs = []
        self.DEPENDENCIES =[]

    def ask_wrong_data(self):
        ans = input("Which output data is not correct? ")
        query = ("select CC.name, CC.id, CC.first_char_line "
                 "from evaluation EVAL "
                 "join code_component CC on EVAL.code_component_id = CC.id " 
                 "where EVAL.repr = ? ")
        code_components = []
        print("Select the invalid evaluation")
        i = 1
        for tupl in self.cursor.execute(query, [ans]):
            print(str(i)+". " + str(tupl[0])+ " = " + ans + " at line " + str(tupl[2]))
            i += 1
            code_components.append(tupl)
        invalid_eval = int(input()) - 1
        invalid_cc = code_components[invalid_eval]
        return CodeComponent(invalid_cc[1], invalid_cc[0], "STARTER")

    
    def prune(self):
        for d in self.DEPENDENCIES:
            source_nodes = self.exec_tree.search_for_node_by_ccid(d.source.id)
            target_nodes = self.exec_tree.search_for_node_by_ccid(d.target.id)
            for sn in source_nodes:
                for tn in target_nodes:
                    sn.prov = True
                    tn.prov = True

    def navigate(self):
        #cc_start = self.ask_wrong_data()
        #self.explore_codecomponent(cc_start)
        self.DEPENDENCIES = self.prov_tools.get_dependencies()
        self.prune()
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def recursive_navigate(self, node: Node):
        if len(node.childrens) == 1:
            self.recursive_navigate(node.childrens[0])

        # Filtering only the childrens that are in provenance dag
        chds = []
        for n in node.childrens:
            if n.prov == True:
                chds.append(n)

        for n in chds:
            if n.validity is Validity.UNKNOWN:
                n = self.evaluate(n)
            if (n.validity is Validity.INVALID):
                for j in chds:
                    if j.validity is Validity.UNKNOWN:
                        j.validity = Validity.VALID
                # re-apply slicing and pruning (?)
                if (n.has_childrens()):
                    self.recursive_navigate(n)


    def evaluate(self, node: Node) -> Node:
        self.exec_tree.node_under_evaluation = node
        vis = Visualization(self.exec_tree)
        vis.view_exec_tree_prov(str(id(node)), self.DEPENDENCIES)
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