from collections import defaultdict

from debugprov.dependency_rel import DependencyRel
from debugprov.evaluation import Evaluation
import logging

class ProvenanceTools:

    def __init__(self, cursor):
        self.cursor = cursor

    
    def flat(self, obj, visited=None):
        visited |= set()
        if id(obj) in visited:
            return
        visited.add(id(obj))
        for e in obj:
            if isinstance(e, list):
                yield from self.flat(e, visited)
            else:
                yield e

    def inplace_flat(self,list_):
        i = 0
        size = len(list_)
        while i < size:
            if isinstance(list_[i], list):
                sublist = list_.pop(i)
                self.inplace_flat(sublist)
                for element in sublist:
                    if element not in list_:
                        list_.append(element)
                size -= 1
            else:
                i += 1
        return list_


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
            key: self.inplace_flat(value)
            for key, value in reachable.items()
        }
        logging.info("Provenance tools # FLAT finished")
        return obj    
        

    def get_dependencies(self):
        original_evaluation = {}
        dependencies = []

        query = '''select EV_INFLU.id as 'EV_INFLU_ID', CC_INFLU.id as 'CC_INFLU_ID', CC_INFLU.type as 'CC_INFLU_TYPEOF', CC_INFLU.name as 'CC_INFLU_NAME', EV_INFLU.checkpoint as 'EV_INFLU_CHECKPOINT', EV_INFLU.member_container_id as 'EV_INFLU_MEMBER_CONTAINER_ID',
        EV_DEPEND.id as 'EV_DEPEND_ID', CC_DEPEND.id as 'CC_DEPEND_ID', CC_DEPEND.type as 'CC_DEPEND_TYPEOF', CC_DEPEND.name as 'CC_DEPEND_NAME', EV_DEPEND.checkpoint as 'EV_DEPEND_CHECKPOINT', EV_DEPEND.member_container_id as 'EV_DEPEND_MEMBER_CONTAINER_ID',
        D.type as 'DEPENDENCY_TYPE' 
        from dependency D 
        join evaluation EV_DEPEND on D.dependent_id = EV_DEPEND.id 
        join evaluation EV_INFLU on D.dependency_id = EV_INFLU.id 
        join code_component CC_DEPEND on EV_DEPEND.code_component_id = CC_DEPEND.id 
        join code_component CC_INFLU on EV_INFLU.code_component_id = CC_INFLU.id  '''
        
        for tupl in self.cursor.execute(query,[]):
            source = Evaluation(tupl[6],tupl[7],tupl[8],tupl[9],tupl[10],tupl[11])
            target = Evaluation(tupl[0],tupl[1],tupl[2],tupl[3],tupl[4],tupl[5])
            dependencies.append(DependencyRel(source,target))
            if tupl[12] == "assignment":
                original_evaluation[tupl[6]] = tupl[0]
        return self.list_to_dict(dependencies), original_evaluation
        #query = ("select EV_INFLU.id as 'EV_INFLU_ID', CC_INFLU.id as 'CC_INFLU_ID', CC_INFLU.type as 'CC_INFLU_TYPEOF', CC_INFLU.name as 'CC_INFLU_NAME', EV_INFLU.checkpoint as 'EV_INFLU_CHECKPOINT', "
        #"EV_DEPEND.id as 'EV_DEPEND_ID', CC_DEPEND.id as 'CC_DEPEND_ID', CC_DEPEND.type as 'CC_DEPEND_TYPEOF', CC_DEPEND.name as 'CC_DEPEND_NAME', EV_DEPEND.checkpoint as 'EV_DEPEND_CHECKPOINT', "
        #"D.type as 'DEPENDENCY_TYPE' "
        #"from dependency D "
        #"join evaluation EV_DEPEND on D.dependent_id = EV_DEPEND.id "
        #"join evaluation EV_INFLU on D.dependency_id = EV_INFLU.id "
        #"join code_component CC_DEPEND on EV_DEPEND.code_component_id = CC_DEPEND.id "
        #"join code_component CC_INFLU on EV_INFLU.code_component_id = CC_INFLU.id " )


    def get_members(self):
        query = '''select m.collection_id,m.key,m.checkpoint,ev.id,cc.id,cc.type,cc.name, ev.checkpoint, ev.member_container_id
        from member m 
        join evaluation ev on ev.id = m.member_id
        join code_component cc on  cc.id = ev.code_component_id '''
       # query = ("select m.collection_id,m.member_id,m.checkpoint,key from member m ")
        members = defaultdict(lambda: defaultdict(dict))
        for tupl in self.cursor.execute(query,[]):
            members[tupl[0]][tupl[1]][tupl[2]] = Evaluation(tupl[3],tupl[4],tupl[5],tupl[6],tupl[7],tupl[8])
        return members
