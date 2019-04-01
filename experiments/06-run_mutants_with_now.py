SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

directories = ['15-decision_tree']

def run_mutants(directories):
    for directory in directories:
        print(directory)
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for content in os.listdir():
                os.chdir(content)
                for py_file in os.listdir():
                        if py_file.endswith('.py'):
                                print(os.getcwd())
                                print("now run {}".format(py_file))
                                proc = subprocess.Popen(['now','run',py_file], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                try:
                                        stdout, stderr = proc.communicate(timeout=TIMEOUT_LIMIT)
                                        returncode = proc.returncode
                                        if returncode == 0:
                                                print("Success running {}".format(py_file))
                                        else:
                                                print(stderr)
                                                import sys
                                                sys.exit("Something wrong happened...")
                                        proc.kill()
                                except:
                                        proc.kill()
                                        import sys
                                        sys.exit("EXCEPT Something wrong happened...")
                os.chdir('..')
        os.chdir('../..')

os.chdir(SCRIPTS_DIRECTORY)
run_mutants(directories)
