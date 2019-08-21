import sys
import os
import subprocess

class NowInterface:

    @staticmethod
    def run_script(command):
        command = command.replace('python ','').split(' ')
        now_call = ['now','run']
        now_call.extend(command)
        proc = subprocess.Popen(now_call, cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if (stdout):
            print(stdout.decode('utf-8'))
        if (stderr):
            print(stderr.decode('utf-8'))
        #print(stdout.decode('utf-8'))
