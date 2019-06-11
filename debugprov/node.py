from debugprov.parameter import Parameter
from debugprov.validity import Validity

class Node:
    
    def __init__(self, ev_id, code_component_id, retrn, name, parent):
        self.ev_id = ev_id
        self.code_component_id = code_component_id
        self.retrn = retrn
        self.name = name
        self.parent = parent
        self.childrens = []
        self.validity = Validity.UNKNOWN
        self.params = []

    def has_childrens(self):
        return len(self.childrens) > 0

    def has_childrens_with_validity(self, validity:Validity):
        for c in self.childrens:
            if c.validity is validity:
                return True
        return False 
    
    def all_childrens_are_valid(self):
        for chd in self.childrens:
            if chd.validity is not Validity.VALID:
                return False
        return True

    def get_parameters(self, cursor):
        query = ("select CC.name, EV.repr as 'value' "
                 "from composition CMP "
                 "join code_component CC on CMP.part_id = CC.id "
                 "join evaluation EV on EV.code_component_id = CC.id "
                 "where CMP.whole_id = ? " 
                 "and CMP.type = ? ")
        for tupl in cursor.execute(query, [self.code_component_id, '*args']):
            self.params.append(Parameter(tupl[0], tupl[1]))

    def get_name(self):
        return "{} {}".format(self.ev_id, self.name)


    def get_all_descendants(self):
        return self._get_all_descendants(self)

    def _get_all_descendants(self, node):
        nodes = []
        nodes.append(node)
        if node.childrens is not None and len(node.childrens) > 0:
            for c in node.childrens:
                nodes.extend(self._get_all_descendants(c))
        return nodes