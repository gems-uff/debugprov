import os
import difflib
from config import Config

config = Config()
config.go_to_scripts_path()

def store_diffs(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        original_file = open(script) 
        original_file_content = original_file.readlines()
        original_file.close()
        os.chdir(config.mutants_with_wrong_result)
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            mutant_file = open("{}.py".format(mutant_dir))
            diff = difflib.ndiff(original_file_content, mutant_file.readlines())
            mutant_file.close()
            diff_file = open(mutant_dir+'.diff','w')
            for idx,d in enumerate(diff):
                diff_file.write(d,)
            diff_file.close()
            os.chdir('..')
        os.chdir('../..')

store_diffs(config.target_scripts)