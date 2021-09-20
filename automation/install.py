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
import sys
import shutil
import subprocess

class InstallRole:
    role = ""

    def get_role_from_working_tree_config(self):
        if os.path.exists(os.path.join('automation','working_tree_config.txt')):
            with open(os.path.join('automation','working_tree_config.txt'), mode='r') as config_file:
                for line in config_file.read().splitlines():
                    if len(line.split()) > 1:
                        if line.split()[0] == "role":
                            self.role = line.split(" ",1)[1]
        if self.role == "":
            self.role = "fresh"

    def write_role(self):
        lines_to_write = [
                "role {0} \n".format(self.role),
                ]
        with open(os.path.join('automation','working_tree_config.txt'),mode='w') as config_file:
            config_file.writelines(lines_to_write)


    def _install_as_developer(self):
        shutil.copyfile("automation/developer-pre-commit.py",".git/hooks/pre-commit")
        subprocess.run(["chmod","+x",".git/hooks/pre-commit"])
        shutil.copyfile("automation/developer-post-commit.py",".git/hooks/post-commit")
        subprocess.run(["chmod","+x",".git/hooks/post-commit"])

    def _install_as_artist(self):
        pass
    
    def _clear_artist_install(self):
        pass

    def _clear_developer_install(self):
        if os.path.exists(os.path.join(".git","hooks","pre-commit")):
            os.replace(os.path.join(".git","hooks","pre-commit"),os.path.join(".git","hooks","pre-commit.sample"))
        if os.path.exists(os.path.join(".git","hooks","post-commit")):
            os.replace(os.path.join(".git","hooks","post-commit"),os.path.join(".git","hooks","post-commit.sample"))

    def install(self):
        if self.role == "developer":
            self._clear_artist_install()
            self._install_as_developer()
        elif self.role == "artist":
            self._clear_developer_install()
            self._install_as_artist()
        elif self.role == "fresh":
            input_role = ""
            while not input_role in ["developer","artist"]:
                input_role = input("Which role to install as? (Allowed values: \"developer\", \"artist\")")
            self.role = input_role
            self.write_role()
            self.install()
            

def run():
    install_role = InstallRole()
    install_role.get_role_from_working_tree_config()
    install_role.install()

if __name__ == "__main__":
    run()

