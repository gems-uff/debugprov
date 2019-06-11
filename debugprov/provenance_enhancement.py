from collections import defaultdict

from debugprov.node import Node
from debugprov.dependency_rel import DependencyRel
from debugprov.validity import Validity
from debugprov.execution_tree import ExecutionTree
from debugprov.visualization import Visualization
from debugprov.provenance_tools import ProvenanceTools
from debugprov.evaluation import Evaluation
from debugprov.context import Context
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
        self.members = self.prov_tools.get_members()
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

    def get_last_print_evid(self):
        query = ("select e.id from evaluation e "
                "join code_component cc on e.code_component_id = cc.id "
                "where cc.name like '%print%' and cc.type='call' "
                "order by cc.first_char_line DESC "
                "LIMIT 1 ")
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception("Could not find print node")
        for tupl in self.cursor.execute(query):
            return tupl[0]

    def get_wrong_data_evid(self,wrong_data):
        wrong_data = "%{}%".format(wrong_data)
        query = ("select e.id from evaluation e "
                "where e.repr like ? "
                "order by e.id DESC "
                "LIMIT 1 ")
        self.cursor.execute(query, [wrong_data])
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception("Could not find wrong node")
        for tupl in self.cursor.execute(query, [wrong_data]):
            return tupl[0]

#    def enhance(self,wrong_node_id):
        #logging.info("Provenance Enhancement # enhance STARTED")
        #logging.info("len(self.dependencies): {}".format(str(len(self.dependencies))))
#        for e in self.dependencies:
#            if e.ev_id == wrong_node_id:
#                wd = e
#        for node in self.exec_tree.get_all_nodes():
#            node.validity = Validity.NOT_IN_PROV
#        search_result = self.exec_tree.search_by_ev_id(wrong_node_id)    
#        if search_result is not None:
#            search_result.validity = Validity.UNKNOWN

    '''    nodes_to_visit = self.dependencies[wd]
        for node in nodes_to_visit:
            self.final_dependencies.append(DependencyRel(node,wd))#
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
        # original: self.final_dependencies.append(DependencyRel(wd,node))
        #self.exec_tree.root_node.validity = Validity.INVALID
        #logging.info("Provenance Enhancement # enhance FINISHED")'''



    def enhance(self,wrong_node_id):
        for e in self.dependencies:
            if e.ev_id == wrong_node_id:
                wd = e
        for node in self.exec_tree.get_all_nodes():
            node.validity = Validity.NOT_IN_PROV
        search_result = self.exec_tree.search_by_ev_id(wrong_node_id)    
        if search_result is not None:
            search_result.validity = Validity.UNKNOWN

        nodes_to_visit = [Context(wd,None)]
        visited = {nodes_to_visit[0]}
        partial_dependencies = []
        while nodes_to_visit:

            context = nodes_to_visit.pop()
            search_result = self.exec_tree.search_by_ev_id(context.evaluation.ev_id)
            if search_result is not None:
                search_result.validity = Validity.UNKNOWN
            for neighbor in self.get_neighborhood(context):
                if neighbor not in visited:
                    visited.add(neighbor)
                    partial_dependencies.append((neighbor.evaluation,context.evaluation))
                    nodes_to_visit.append(neighbor)


        reachable = defaultdict(list)
        for target, source in partial_dependencies:
            target_node = self.exec_tree.search_by_ev_id(target.ev_id)
            if target_node: # if is a function call
                reachable[source].append(target)
                #print(source, target)
            else:
                reachable[source].append(reachable[target])


        for source, values in reachable.items():
            source_node = self.exec_tree.search_by_ev_id(source.ev_id)
            if source_node:
                for target in self.prov_tools.flat(values, visited=set()):
                    if source != target:
                        self.final_dependencies.append(DependencyRel(target, source))

        

        self.exec_tree.dependencies = set(self.final_dependencies)

    def get_neighborhood(self,context):

        if context.is_activation:
            return

        node = context.evaluation
        checkpoint = context.checkpoint
        # If time is not in the context, get it from the entity
        # ToDo: verificar se nao tem que voltar para a definicao de evaluation
        checkpoint = checkpoint or node.checkpoint
        
        # Follow default derivations
        for d in self.dependencies.get(node, []):
            checkpoint = checkpoint or d.checkpoint
            yield Context(d, None)
        
        # Yield non-navigatable activation
        #activation_node = self.exec_tree.search_by_ev_id(node.activation_id) 
        #if activation_node:
        #    yield Context(
        #        Evaluation(node.activation_id, None, node.code_component_id, None, node.code_component_name, None, None),
        #        None, True
        #    )
        

        if checkpoint:
            # Get initial reference to value
            original = node.member_container_id
            #original, result = get_original_reference(n)

            # Move to all parts of the structure 
            # Reconstruct state
            keys = self.members.get(original, {})
            state = {}
            for key, checkpoints in keys.items():
                value = max(
                    ((member_checkpoint, evaluation)
                    for member_checkpoint, evaluation in checkpoints.items()
                    if member_checkpoint <= checkpoint),
                    key=lambda e: e[0],
                    default=None
                )
                if value is not None:
                    state[key] = value

            # Move to parts of the state
            for member_checkpoint, evaluation in state.values():
                yield Context(evaluation, checkpoint)



    def enhance_all(self):
        #self.exec_tree.root_node.validity = Validity.INVALID
        dependencies = []
        for source in self.dependencies:
            if source.code_component_type == 'call':
                for target in self.dependencies[source]:
                    dependencies.append(DependencyRel(source,target))
        self.exec_tree.dependencies = dependencies
