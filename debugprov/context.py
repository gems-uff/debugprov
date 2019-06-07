class Context:

    def __init__(self,evaluation,checkpoint,is_activation=False):
        self.evaluation = evaluation
        self.checkpoint = checkpoint
        self.is_activation = is_activation 


    def __eq__(self, other):
        if isinstance(other, Context):
            return (
            	self.evaluation, self.checkpoint, self.is_activation
            ) == (
            	other.evaluation, other.checkpoint, other.is_activation
            )
        return False

    def __hash__(self):
        return hash((self.evaluation.ev_id, self.checkpoint, self.is_activation))    