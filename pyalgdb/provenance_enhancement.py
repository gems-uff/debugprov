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
        ans = input("Which output data is not correct? ")
        query = ("select EVAL.id, CC.id, CC.type "
                 "from evaluation EVAL "
                 "join code_component CC on EVAL.code_component_id = CC.id " 
                 "where EVAL.repr = ? ")
        evals = []
        for tupl in self.cursor.execute(query, [ans]):
            evals.append(Evaluation(tupl[0],tupl[1],tupl[2]))
        return evals[-1]

    def is_in(self, dep:DependencyRel, dependencies):
      for d in dependencies:
            if dep.target.ev_id == d.target.ev_id and dep.source.ev_id == d.source.ev_id:
                  return True
      return False
   
    def insert_dependency(self, dep, dependency_list):
        if not self.is_in(dep, dependency_list):
            dependency_list.append(dep)

    def build_provenance_dag(self, ev_id):
        for d in self.dependencies:
            if d.target.ev_id == ev_id:
                self.insert_dependency(d, self.filtered_dependencies)
                self.build_provenance_dag(d.source.ev_id)

    def find_influencers_of(self, ev_id):
        arr = []
        for d in self.filtered_dependencies:
            if d.target.ev_id == ev_id:
                arr.append(d.source)
        return arr
                

    def get_func_dependencies_of(self, ev_id):
        func_dependencies = []
        evaluations = self.find_influencers_of(ev_id)
        for ev in evaluations:
            if ev.code_component_type == 'call':
                func_dependencies.append(ev)
            else:
                func_dependencies.extend(self.get_func_dependencies_of(ev.ev_id))
        return func_dependencies


    def recursive_get_func_dependencies_of(self, evaluation):
        evaluations = self.get_func_dependencies_of(evaluation.ev_id)
        for ev in evaluations:
            self.insert_dependency(DependencyRel(ev, evaluation), self.final_dependencies)
            self.recursive_get_func_dependencies_of(ev)

    def enhance(self, evaluation):
        self.build_provenance_dag(evaluation.ev_id)
        self.recursive_get_func_dependencies_of(evaluation)    
        return self.final_dependencies    

