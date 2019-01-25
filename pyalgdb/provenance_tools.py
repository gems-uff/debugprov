
from pyalgdb.code_component import CodeComponent
from pyalgdb.dependency_rel import DependencyRel



class ProvenanceTools:

    def __init__(self, cursor):
        self.cursor = cursor

    def get_dependencies(self):
        dependencies = []
        query = ("select CC_INFLU.id, CC_INFLU.name, CC_INFLU.type, "
        "CC_DEPEND.id, CC_DEPEND.name, CC_DEPEND.type "
        "from dependency D "
        "join evaluation EV_DEPEND on D.dependent_id = EV_DEPEND.id "
        "join evaluation EV_INFLU on D.dependency_id = EV_INFLU.id "
        "join code_component CC_DEPEND on EV_DEPEND.code_component_id = CC_DEPEND.id "
        "join code_component CC_INFLU on EV_INFLU.code_component_id = CC_INFLU.id " )
        for tupl in self.cursor.execute(query,[]):
                dependent = CodeComponent(tupl[3],tupl[4],tupl[5])
                influencer = CodeComponent(tupl[0],tupl[1],tupl[2])
                dependencies.append(DependencyRel(dependent, influencer))
        return dependencies

