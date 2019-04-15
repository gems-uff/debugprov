import sys
import os
import subprocess
import traceback
from config import Config

config = Config()


ans = raw_input("TYPE OK TO RUN \n")
    if ans != 'ok':
        sys.exit()

#####################
# 01-run_scripts.py
#####################
try:
    proc = subprocess.Popen(['python','01-run_scripts.py'], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stdout.decode('utf-8'))
except:
    traceback.print_exc()


#####################
# 03-run_mutants.py
#####################
try:
    proc = subprocess.Popen(['python','03-run_mutants.py'], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stdout.decode('utf-8'))
except:
    traceback.print_exc()

