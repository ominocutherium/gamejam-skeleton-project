#!/usr/bin/env python3

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
                for line in post_commit_file:
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
