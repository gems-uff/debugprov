from debugprov.node import Node
from debugprov.dependency_rel import DependencyRel
from debugprov.validity import Validity
from debugprov.execution_tree import ExecutionTree
from debugprov.visualization import Visualization
from debugprov.provenance_tools import ProvenanceTools
from debugprov.evaluation import Evaluation
#import logging

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

    def enhance(self,wrong_node_id):
        #logging.info("Provenance Enhancement # enhance STARTED")
        #logging.info("len(self.dependencies): {}".format(str(len(self.dependencies))))
        for e in self.dependencies:
            if e.ev_id == wrong_node_id:
                wd = e
        for node in self.exec_tree.get_all_nodes():
            node.validity = Validity.NOT_IN_PROV
        search_result = self.exec_tree.search_by_ev_id(wrong_node_id)    
        if search_result is not None:
            search_result.validity = Validity.UNKNOWN
            
        nodes_to_visit = self.dependencies[wd]
        for node in nodes_to_visit:
            self.final_dependencies.append(DependencyRel(wd,node))
        for node in nodes_to_visit:
            search_result = self.exec_tree.search_by_ev_id(node.ev_id)
            if search_result is not None:
                search_result.validity = Validity.UNKNOWN
            node.visited = True
            if node in self.dependencies:
                for n in self.dependencies[node]:
                    self.final_dependencies.append(DependencyRel(n,node))
                    if not hasattr(n,'visited'):
                        nodes_to_visit.append(n)
        self.exec_tree.dependencies = set(self.final_dependencies)
        self.exec_tree.root_node.validity = Validity.INVALID
        #logging.info("Provenance Enhancement # enhance FINISHED")

    def enhance_all(self):
        self.exec_tree.root_node.validity = Validity.INVALID
        dependencies = []
        for source in self.dependencies:
            if source.code_component_type == 'call':
                for target in self.dependencies[source]:
                    dependencies.append(DependencyRel(source,target))
        self.exec_tree.dependencies = dependencies
