#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import subprocess
import json

class StagedPathsInCommit:
    paths = []
    game_files_changed = False
    assets_changed = False
    website_changed = False
    docs_changed = False
    automation_code_changed = False

    def __init__(self):
        self.paths = []

    def declare(self):
        print("Game files changed: {0}".format(self.game_files_changed))
        print("Game assets changed: {0}".format(self.assets_changed))
        print("Documentation changed: {0}".format(self.website_changed))
        print("Website changed: {0}".format(self.docs_changed))
        print("Scripts changed: {0} (note: should not share commits with other)".format(self.automation_code_changed))

    def dump(self):
        return json.dumps({
            "game_files_changed":self.game_files_changed,
            "assets_changed":self.assets_changed,
            "website_changed":self.website_changed,
            "docs_changed":self.docs_changed,
            "automation_code_changed":self.automation_code_changed,
            })

    def query_tree_for_staged_paths(self):
        git_status_call = subprocess.run(["git","status","--porcelain"],capture_output=True)
        lines = git_status_call.stdout.decode().splitlines()
        for line in lines:
            if line[0] != ' ' and line[:2] != '??':
                self.paths.append(line.split()[1])

    def verify_only_content_or_automation_changes_staged_not_both(self):
        if self.game_files_changed or self.assets_changed or self.docs_changed or self.website_changed:
            if self.automation_code_changed:
                return false
        return true


    def evaluate_staged_paths(self):
        for path in self.paths:
            if path.startswith('automation/') and path.endswith('.py'):
                self.automation_code_changed = True
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
