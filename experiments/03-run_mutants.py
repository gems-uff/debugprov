import os
import subprocess

SCRIPTS_DIRECTORY = 'scripts'
TIMEOUT_LIMIT = 90

os.chdir(SCRIPTS_DIRECTORY)

mutants = ['04-lu_decomposition/mutants.running']

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
                        print(stderr)
                    proc.kill()
                except:
                    muts_with_infinite_loops.append(mutant)
                    proc.kill()
        for mut in muts_with_syntax_errors:
            os.remove(mut)
        for mut in muts_with_infinite_loops:
            os.remove(mut)
        print("Deleted {} mutants with syntax errors".format(len(muts_with_syntax_errors)))
        print("Deleted {} mutants with infinite loops".format(len(muts_with_infinite_loops)))
        os.chdir('../..')

run_mutants(mutants)