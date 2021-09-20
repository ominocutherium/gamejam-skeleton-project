#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2021 ominocutherium
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
# 
# Part of ominocutherium's godot gamejam skeleton project.

import os
import subprocess

class PreCommitCI:
    test_dirs = []
    use_beta = False
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
        if self.use_beta:
            self.call_params[0] = self.beta_exec_name
        else:
            self.call_params[0] = self.stable_exec_name
        return subprocess.call(self.call_params)

def run():
    ci = PreCommitCI()
    return ci.run()

