class Evaluation:

    def __init__(self, ev_id, code_component_id, code_component_type, code_component_name,checkpoint,member_container_id):
        self.ev_id = ev_id
        self.code_component_id = code_component_id
        self.code_component_type = code_component_type
        self.code_component_name = code_component_name
        self.checkpoint = checkpoint
        self.member_container_id = member_container_id

    def __eq__(self, other):
        if isinstance(other, Evaluation):
            return self.ev_id == other.ev_id
        return False

    def __hash__(self):
        return hash(self.ev_id)