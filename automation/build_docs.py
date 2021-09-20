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

class DocsState:
    docs_default_files = []

    def __init__(self):
        self.docs_default_files = []

    def get_defaults_from_config(self):
        if os.path.exists(os.path.join('automation','config.txt')):
            with open(os.path.join('automation','config.txt')) as config_file:
                for line in config_file:
                    if len(line.split()) > 1:
                        if line.split()[0] == "docs_defaults":
                            self.docs_default_files.append(line.split()[1])

    def compile_all_docs(self):
        home_dir = os.getcwd()
        os.chdir('docs')
        for defaults_file in self.docs_default_files:
            process = subprocess.run(['pandoc','-d',defaults_file])
        os.chdir(home_dir)

def run():
    state = DocsState()
    state.get_defaults_from_config()
    state.compile_all_docs()

if __name__ == "__main__":
    run()
