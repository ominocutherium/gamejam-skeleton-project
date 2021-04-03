#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import subprocess

class StagedPathsInCommit:
    paths = []
    game_files_changed = False
    assets_changed = False
    website_changed = False
    docs_changed = False

    def __init__(self):
        self.paths = []

    def query_tree_for_staged_paths(self):
        git_status_call = subprocess.run(["git","status","--porcelain"],capture_output=True)
        lines = git_status_call.stdout.decode().splitlines()
        for line in lines:
            if line[0] != ' ' and line[:2] != '??':
                self.paths.append(line.split()[1])

    def evaluate_staged_paths(self):
        for path in self.paths:
            if path.startswith('automation/') and path.endswith('.py'):
                self.automation_scripts_changed = True
            elif path.startswith('docs/') and path.endswith(('.md','.yaml')):
                self.docs_changed = True
            elif path.startswith('website/') and path.endswith(('.md','.yaml',".css",".png",".gif",".jpg",".svg",".js")):
                self.website_changed = True
            elif path.startswith('game/'):
                if path.endswith(('.png','.tres','.shader')):
                    self.assets_changed = True
                else:
                    self.game_files_changed = True

def run():
    staged_paths = StagedPathsInCommit()
    staged_paths.query_tree_for_staged_paths()
    staged_paths.evaluate_staged_paths()
    return staged_paths
