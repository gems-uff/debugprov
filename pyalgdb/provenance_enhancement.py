from pyalgdb.navgiation_strategy import NavigationStrategy
from pyalgdb.node import Node
from pyalgdb.code_component import CodeComponent
from pyalgdb.dependency_rel import DependencyRel
from pyalgdb.validity import Validity
from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.visualization import Visualization
from pyalgdb.provenance_tools import ProvenanceTools
from pyalgdb.evaluation import Evaluation

class ProvenanceEnhancement(NavigationStrategy):

    def __init__(self, exec_tree: ExecutionTree, cursor):
        super().__init__(exec_tree)
        self.prov_tools = ProvenanceTools(cursor)
        self.cursor = cursor
        self.dependencies =[]
        self.filtered_dependencies = []

    def ask_wrong_data(self):
        ans = input("Which output data is not correct? ")
        query = ("select EVAL.id, CC.id "
                 "from evaluation EVAL "
                 "join code_component CC on EVAL.code_component_id = CC.id " 
                 "where EVAL.repr = ? ")
        evals = []
        for tupl in self.cursor.execute(query, [ans]):
            evals.append(Evaluation(tupl[0], tupl[1]))
        return evals[-1]

    def search_influencers_of(self, ev_id):
        for d in self.dependencies:
            if d.target.ev_id == ev_id:
                self.filtered_dependencies.append(d)
                self.search_influencers_of(d.source.ev_id)

    def enhance(self, evaluation):
        self.search_influencers_of(evaluation.ev_id)
        

    
