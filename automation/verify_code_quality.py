#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import os
import subprocess

class PreCommitCI:
    test_dirs = []
    use_beta = True
    stable_exec_name = "godot"
    beta_exec_name = "godot-beta"
    call_params = ["godot","-d","-s","--path","game/","addons/gut/gut_cmdln.gd","-gexit_on_success","-gignore_pause","-gprefix=test_","-gsuffix=.gd"]

    def __init__(self):
        self.test_dirs = []

    def get_test_dirs_from_config(self):
        if os.path.exists(os.path.join('automation','config.txt')):
            with open(os.path.join('automation','config.txt')) as config:
                for line in config:
                    if len(line.split()) > 1:
                        if line.split()[0] == "test_dir":
                            self.test_dirs.append(line.split()[1])

    def run(self):
        self.get_test_dirs_from_config()
        return self.run_tests()

    def run_tests(self):
        dir_param = "-gdir="
        for dir_name in self.test_dirs:
            dir_param += 'res://' + dir_name + ','
        self.call_params.append(dir_param)
        if use_beta:
            self.call_params[0] = self.beta_exec_name
        else:
            self.call_params[0] = self.stable_exec_name
        return subprocess.call(self.call_params)

def run():
    ci = PreCommitCI()
    return ci.run()

