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
        self.final_dependencies = []
        

    def ask_wrong_data(self):
        ans = input("Which evaluation id is not correct? ")
        query = ("select EVAL.id, CC.id, CC.type, CC.name "
                 "from evaluation EVAL "
                 "join code_component CC on EVAL.code_component_id = CC.id " 
                 "where EVAL.id = ? ")
        evals = []
        for tupl in self.cursor.execute(query, [ans]):
            evals.append(Evaluation(tupl[0],tupl[1],tupl[2],tupl[3]))
        return evals[-1]

    def is_in(self, dep:DependencyRel, dependencies):
      for d in dependencies:
            if dep.influencer.ev_id == d.influencer.ev_id and dep.dependent.ev_id == d.dependent.ev_id:
                  return True
      return False
   
    def insert_dependency(self, dep, dependency_list):
        if not self.is_in(dep, dependency_list):
            dependency_list.append(dep)

    def find_influencers_of(self, ev_id):
        arr = []
        for d in self.dependencies:
            if d.dependent.ev_id == ev_id:
                arr.append(d.influencer)
        return arr

    def get_influencers_of(self, ev_id, typeof):
        influencers = []
        evaluations = self.find_influencers_of(ev_id)
        for ev in evaluations:
            if ev.code_component_type == typeof:
                influencers.append(ev)
            else:
                influencers.extend(self.get_influencers_of(ev.ev_id, typeof))
        return influencers        

    def recursive_get_func_dependencies_of(self, evaluation):
        influencers = self.get_influencers_of(evaluation.ev_id, 'call')
        for ev in influencers:
            self.insert_dependency(DependencyRel(ev, evaluation), self.final_dependencies)
            self.recursive_get_func_dependencies_of(ev)

    def enhance(self, evaluation):
        self.recursive_get_func_dependencies_of(evaluation)    
        return self.final_dependencies    
