#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import os
import sys

sys.path.append(os.getcwd())

import automation.verify_staged_paths_in_commit as v_st_path
import automation.verify_code_quality as tests


def run():
    staged_paths = v_st_path.run()
    if not staged_paths.verify_only_content_or_automation_changes_staged_not_both():
        print("If you are making changes to your game project, you should not be making changes to the automation scripts. Hook scripts and sync tools should be kept as separate commits for the purposes of also being committed to upstream.")
        sys.exit(1)
    if staged_paths.game_files_changed:
        if not tests.run():
            sys.exit(1)
    with open(os.path.join('automation','post_commit.json'),mode='w') as what_changed:
            what_changed.writeline(staged_paths.dump())

if __name__ == "__main__":
    run()
