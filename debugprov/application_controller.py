import os.path

from debugprov.config import Config
from debugprov.now_storage_interface import NowStorageInterface
from debugprov.console_interface import ConsoleInterface
from debugprov.now_interface import NowInterface
from debugprov.execution_tree_creator import ExecTreeCreator

class ApplicationController:

    def run(self):
        if os.path.exists(Config.NOW2_DEFAULT_SQL_PATH):
            storage = NowStorageInterface()
            storage.connect(Config.NOW2_DEFAULT_SQL_PATH)
            trials = storage.get_trials()
            trial_id = ConsoleInterface.select_trial(trials)
            storage.trial_id = trial_id
            execTreeCreator = ExecTreeCreator(storage)
            execTreeCreator.create_exec_tree()

        else:
            command = ConsoleInterface.get_run_command()
            NowInterface.run_script(command)
            
