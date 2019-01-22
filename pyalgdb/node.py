from pyalgdb.parameter import Parameter
from pyalgdb.validity import Validity

class Node:
    
    def __init__(self, id, code_component_id, retrn, name, parent):
        self.id = id
        self.code_component_id = code_component_id
        self.retrn = retrn
        self.name = name
        self.parent = parent
        self.childrens = []
        self.validity = Validity.UNKNOWN
        self.params = []
        self.prov = None

    def has_childrens(self):
        return len(self.childrens) > 0

    def has_childrens_with_validity(self, validity:Validity):
        for c in self.childrens:
            if c.validity is validity:
                return True
        return False 

    def get_parameters(self, cursor):
        query = ("select CC.name, EV.repr as 'value' "
                 "from composition CMP "
                 "join code_component CC on CMP.part_id = CC.id "
                 "join evaluation EV on EV.code_component_id = CC.id "
                 "where CMP.whole_id = ? " 
                 "and CMP.type = ? ")
        for tupl in cursor.execute(query, [self.code_component_id, '*args']):
            self.params.append(Parameter(tupl[0], tupl[1]))
