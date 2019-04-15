import os
import subprocess
import shutil
from config import Config

TIMEOUT_LIMIT = 90

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

# Move all mutants from mutants.all to mutants.running
def move_mutants():
    os.mkdir(config.running_mutants_dir)
    copytree(config.all_mutants_dir,config.running_mutants_dir)

def run_mutants(scripts):
    muts_with_syntax_errors = []
    muts_with_infinite_loops = []
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        os.chdir(directory)
        move_mutants()
        os.chdir(config.running_mutants_dir)
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

run_mutants(config.target_scripts)
config.go_back_to_current_path()