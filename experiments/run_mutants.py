SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

mutants = ['02-bisection/mutants.all']

def run_mutants(scripts):
    muts_with_syntax_errors = []
    muts_with_infinite_loops = []
    for script_path in scripts:
        print(script_path)
        os.chdir(script_path)
        for mutant in os.listdir():
            if mutant.endswith('.py'):
                print(mutant)
                proc = subprocess.Popen(['python',mutant], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    stdout, stderr = proc.communicate(timeout=TIMEOUT_LIMIT)
                    returncode = proc.returncode
                    if returncode == 0:
                        logfile = open(mutant+'.log','w') 
                        logfile.write(stdout.decode('utf-8'))
                        logfile.close()
                    else:
                        muts_with_syntax_errors.append(mutant)
                except:
                    muts_with_infinite_loops.append(mutant)
        for mut in muts_with_syntax_errors:
            os.remove(mut)
        for mut in muts_with_infinite_loops:
            os.remove(mut)
        print("Deleted {} mutants with syntax errors".format(len(muts_with_syntax_errors)))
        print("Deleted {} mutants with infinite loops".format(len(muts_with_infinite_loops)))
        os.chdir('../..')

os.chdir(SCRIPTS_DIRECTORY)
run_mutants(mutants)