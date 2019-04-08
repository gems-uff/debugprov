SCRIPTS_DIRECTORY = 'scripts'

import os
import subprocess
import shutil

os.chdir(SCRIPTS_DIRECTORY)

directories = ['08-edit_distance']

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
run_mutants(directories)