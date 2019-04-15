import os
import subprocess
import shutil
from config import Config

config = Config()
config.go_to_scripts_path()

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

# Move all mutants from mutants.running to mutants.wrong_result
def move_mutants():
    os.mkdir(config.mutants_with_wrong_result)
    copytree(config.running_mutants_dir,config.mutants_with_wrong_result)

def check_results(scripts):
    for script_path in scripts:
        muts_with_correct_results = []
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        script_log = "{}.log".format(script)
        os.chdir(directory)
        move_mutants()
        original_log_file = open(script_log) 
        original_result = original_log_file.readlines()
        original_log_file.close()
        os.chdir(config.mutants_with_wrong_result)
        for a_file in os.listdir():
            if a_file.endswith('.log'):
                logfile = open(a_file,'r')
                content = logfile.readlines()
                logfile.close()
                if content == original_result:
                    muts_with_correct_results.append(a_file)
        print('len muts_with_correct_results ')
        print(len(muts_with_correct_results))
        for mut in muts_with_correct_results:
            os.remove(mut[:-4])
            os.remove(mut)
        os.chdir('../..')
        muts_with_correct_results = []
        print()

check_results(config.target_scripts)
config.go_to_scripts_path()