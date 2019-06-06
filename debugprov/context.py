class Context:

    def __init__(self,evaluation,checkpoint):
        self.evaluation = evaluation
        self.checkpoint = checkpoint


    def __eq__(self, other):
        if isinstance(other, Context):
            return self.evaluation, self.checkpoint == other.evaluation, other.checkpoint
        return False

    def __hash__(self):
        return hash((self.evaluation.ev_id, self.checkpoint))    