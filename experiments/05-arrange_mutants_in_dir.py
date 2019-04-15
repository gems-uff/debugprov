import os
import subprocess
import shutil

from config import Config

config = Config()
config.go_to_scripts_path()

def arrange_mutants(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
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

arrange_mutants(config.target_scripts)