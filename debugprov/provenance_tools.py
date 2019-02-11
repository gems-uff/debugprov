from debugprov.dependency_rel import DependencyRel
from debugprov.evaluation import Evaluation

class ProvenanceTools:

    def __init__(self, cursor):
        self.cursor = cursor

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
                dependent = Evaluation(tupl[4],tupl[5],tupl[6],tupl[7])
                influencer = Evaluation(tupl[0],tupl[1],tupl[2],tupl[3])
                dependencies.append(DependencyRel(influencer,dependent))
        return dependencies
