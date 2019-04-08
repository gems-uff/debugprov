SCRIPTS_DIRECTORY = 'scripts'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'

import os
import subprocess
from datetime import datetime

programs = [
           '02-bisection',
           '03-intersection',
           #'04-lu_decomposition
           '05-newton_method',
        ]

os.chdir(SCRIPTS_DIRECTORY)

for program in programs:
    os.chdir(program)
    try:
        print("{} - Running experiments from {}".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f'),program))
        proc = subprocess.Popen(['python','Experiment.py'], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        print("{} - Done".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
    except:
        print("{} - Something went wrong".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
    os.chdir('..')