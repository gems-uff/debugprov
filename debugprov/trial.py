class Trial:

    def __init__(self, trial_id, script, start, finish, command, path):
        self.trial_id = trial_id
        self.script = script
        self.start = start
        self.finish = finish
        self.command = command
        self.path = path

    def __str__(self):
        return ('Trial {}: {} \n'
                '\twith code hash NNNNNNNNNNNNNN \n'
                '\tran from {} to {} \n'
                '\tduration: JJJJJJJJJJJJJJJJ\n').format(self.trial_id,self.command,self.start,self.finish)

