#!/usr/bin/env python3

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
                for line in config_file:
                    if len(line.split()) > 1:
                        if line.split()[0] == "role":
                            self.role = line.split(" ",1)[1]
        else:
            self.role = "fresh"

    def write_role(self):
        with open(os.path.join('automation','working_tree_config.txt'),mode='w') as config_file:
            config_file.write("role {0}".format(self.role))


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
            os.replace(os.path.join(".git","hooks","post-commit"),os.path.join(".git","hooks","pre-commit.sample"))

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

