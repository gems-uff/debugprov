import shutil
import subprocess
import os
SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30


directories = ['14-rsa_cipher']


def run_mutants(directories):
    for directory in directories:
        print(directory)
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for subdir in os.listdir():
            if os.path.isdir(subdir):
                shutil.copy('cryptomath_module.py',subdir+'/cryptomath_module.py')
                shutil.copy('rabin_miller.py',subdir+'/rabin_miller.py')
                shutil.copy('rsa_key_generator.py',subdir+'/rsa_key_generator.py')
                shutil.copy('rsa_privkey.txt',subdir+'/rsa_privkey.txt')
                shutil.copy('rsa_pubkey.txt',subdir+'/rsa_pubkey.txt')

        os.chdir('../..')


os.chdir(SCRIPTS_DIRECTORY)
run_mutants(directories)
