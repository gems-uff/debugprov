SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

directories = ['14-rsa_cipher']

def run_mutants(directories):
    for directory in directories:
        print(directory)
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for py_file in os.listdir():
            if py_file.endswith('.py'):
                dir_name = py_file[:-3]
                os.mkdir(dir_name)
                cwd = os.getcwd()
                shutil.move("{}/{}".format(cwd,py_file), "{}/{}/{}".format(cwd,dir_name,py_file))
                print("{}/{}".format(cwd,py_file) + ' -> ' + "{}/{}/{}".format(cwd,dir_name,py_file))
                logfile = "{}{}".format(py_file,'.log')
                shutil.move("{}/{}".format(cwd,logfile), "{}/{}/{}".format(cwd,dir_name,logfile))
                print("{}/{}".format(cwd,logfile) + ' -> ' + "{}/{}/{}".format(cwd,dir_name,logfile))
        os.chdir('../..')
os.chdir(SCRIPTS_DIRECTORY)
run_mutants(directories)