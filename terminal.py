#!/usr/local/bin/python

import os
import subprocess

while(True):
    # cntrl-c to quit
    current_dir = os.getcwd()
    command = input(f"{current_dir}$")

    if command[:2] == 'cd':
        os.chdir(command[3:])

    if command == 'exit':
        break

    process = subprocess.Popen(command, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    out, err = process.communicate()

    print(out)
    print(err)