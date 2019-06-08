from debugprov.evaluation import Evaluation

# Defines a dependency relation between two evalautions

class DependencyRel:
    
    def __init__(self, source: Evaluation, target: Evaluation):
        self.source = source
        self.target = target

    def __eq__(self, other):
        if isinstance(other, DependencyRel):
            if self.source == other.source and self.target == other.target:
                return True
        return False

    def __hash__(self):
        str(self.source.ev_id)+str(self.target.ev_id)
        return hash(str(self.source.ev_id)+str(self.target.ev_id))
