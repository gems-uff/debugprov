from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.code_component import CodeComponent
from pyalgdb.dependency_rel import DependencyRel
from pyalgdb.validity import Validity
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.visualization import Visualization
from pyalgdb.provenance_tools import ProvenanceTools

class ProvenanceEnhancement(NavigationStrategy):

    def __init__(self, exec_tree: ExecutionTree, cursor):
        super().__init__(exec_tree)
        self.prov_tools = ProvenanceTools(cursor)
        self.cursor = cursor
        self.dependencies =[]

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

    def enhance(self):
        for d in self.dependencies:
            source_nodes = self.exec_tree.search_by_ev_id(d.source.ev_id)
            target_nodes = self.exec_tree.search_by_ev_id(d.target.ev_id)
            for sn in source_nodes:
                for tn in target_nodes:
                    sn.prov = True
                    tn.prov = True
