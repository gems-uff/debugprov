class Evaluation:

    def __init__(self, strings):
        self.trial_id = strings[0]
        self.id = strings[1]
        self.checkpoint = strings[2]
        self.code_component_id = strings[3]
        self.activation_id = strings[4]
        self.repr = strings[5]