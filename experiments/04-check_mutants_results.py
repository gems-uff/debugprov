import os
import subprocess

SCRIPTS_DIRECTORY = 'scripts'

os.chdir(SCRIPTS_DIRECTORY)

scripts = ['08-edit_distance/edit_distance.py.log']

def check_results(scripts):
    for script_path in scripts:
        muts_with_correct_results = []
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        original_log_file = open(script) 
        original_result = original_log_file.readlines()
        original_log_file.close()
        os.chdir('mutants.wrong_result')
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

check_results(scripts)