import os
import subprocess
import shutil

SCRIPTS_DIRECTORY = 'scripts'
TIMEOUT_LIMIT = 90

os.chdir(SCRIPTS_DIRECTORY)

directories = ['04-lu_decomposition']

def run_mutants_with_now(directories):
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

run_mutants_with_now(directories)