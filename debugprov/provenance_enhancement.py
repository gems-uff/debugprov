from debugprov.node import Node
from debugprov.dependency_rel import DependencyRel
from debugprov.validity import Validity
from debugprov.execution_tree import ExecutionTree
from debugprov.visualization import Visualization
from debugprov.provenance_tools import ProvenanceTools
from debugprov.evaluation import Evaluation

class ProvenanceEnhancement():

    FUNCTION_CALL = 'call'
    
    QUERY = ("select EVAL.id, CC.id, CC.type, CC.name "
             "from evaluation EVAL "
             "join code_component CC on EVAL.code_component_id = CC.id " 
             "where EVAL.id = ? ")

    def __init__(self, exec_tree: ExecutionTree, cursor):
        self.exec_tree = exec_tree
        self.prov_tools = ProvenanceTools(cursor)
        self.cursor = cursor
        self.dependencies = self.prov_tools.get_dependencies()
        self.exec_tree.dependencies = self.dependencies
        self.filtered_dependencies = []
        self.final_dependencies = []
        

    def ask_wrong_data(self):
        ans = input("Which evaluation id is not correct? ")
        query = self.QUERY
        evals = []
        for tupl in self.cursor.execute(query, [ans]):
            evals.append(Evaluation(tupl[0],tupl[1],tupl[2],tupl[3]))
        return evals[-1]

    def enhance(self,wrong_eval):
        self.recursive_enhance(wrong_eval) 
        self.exec_tree.root_node.validity = Validity.INVALID
        self.exec_tree.dependencies = self.final_dependencies

        
    
    def recursive_enhance(self,current):
        conj = self.dependencies[current]
        for c in conj:
            self.final_dependencies.append(DependencyRel(c,current))
            self.recursive_enhance(c)
        
        

    def enhance_all(self):
        self.exec_tree.root_node.validity = Validity.INVALID
        dependencies = []
        for source in self.dependencies:
            if source.code_component_type == 'call':
                for target in self.dependencies[source]:
                    dependencies.append(DependencyRel(source,target))
        self.exec_tree.dependencies = dependencies
