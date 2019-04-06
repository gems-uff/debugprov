from collections import defaultdict

from debugprov.dependency_rel import DependencyRel
from debugprov.evaluation import Evaluation
import logging

class ProvenanceTools:

    def __init__(self, cursor):
        self.cursor = cursor

    def flat(self, list_):
        for element in list_:
            if isinstance(element, list):
                yield from self.flat(element)
            else:
                yield element

    def list_to_dict(self, dependencies):
        logging.info("Provenance tools # list_to_dict STARTED")
        logging.info('len(dependencies): {}'.format(len(dependencies)))
        reachable = defaultdict(list)
        for dep in dependencies:
            if dep.target.code_component_type == 'call': # if is a function call
                reachable[dep.source].append(dep.target)
            else:
                reachable[dep.source].append(reachable[dep.target])
        logging.info("Provenance tools # list_to_dict FINISHED")    
        logging.info("Provenance tools # FLAT starting..")    
        obj = {
            key: set(self.flat(value))
            for key, value in reachable.items()
        }
        logging.info("Provenance tools # FLAT finished")
        return obj    
        

    def get_dependencies(self):
        dependencies = []
        query = ("select EV_INFLU.id as 'EV_INFLU_ID', CC_INFLU.id as 'CC_INFLU_ID', CC_INFLU.type as 'CC_INFLU_TYPEOF', CC_INFLU.name as 'CC_INFLU_NAME', "
        "EV_DEPEND.id as 'EV_DEPEND_ID', CC_DEPEND.id as 'CC_DEPEND_ID', CC_DEPEND.type as 'CC_DEPEND_TYPEOF', CC_DEPEND.name as 'CC_DEPEND_NAME' "
        "from dependency D "
        "join evaluation EV_DEPEND on D.dependent_id = EV_DEPEND.id "
        "join evaluation EV_INFLU on D.dependency_id = EV_INFLU.id "
        "join code_component CC_DEPEND on EV_DEPEND.code_component_id = CC_DEPEND.id "
        "join code_component CC_INFLU on EV_INFLU.code_component_id = CC_INFLU.id " )
        for tupl in self.cursor.execute(query,[]):
                source = Evaluation(tupl[4],tupl[5],tupl[6],tupl[7])
                target = Evaluation(tupl[0],tupl[1],tupl[2],tupl[3])
                dependencies.append(DependencyRel(source,target))
        return self.list_to_dict(dependencies)
