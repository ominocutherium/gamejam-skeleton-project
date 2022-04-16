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

sys.path.append(os.getcwd())

import automation.verify_staged_paths_in_commit as v_st_path
import automation.verify_code_quality as tests
import automation.script_unit_tests as script_tests
import automation.verify_branch_is_primary as primary

def run():
    if not primary.run():
        print("Not the primary branch ({}). Skipping hooks.".format(primary.get_primary_branchname_from_config()))
        return
    staged_paths = v_st_path.run()
    if not staged_paths.verify_only_content_or_automation_changes_staged_not_both():
        print("If you are making changes to your game project, you should not be making changes to the automation scripts. Hook scripts and sync tools should be kept as separate commits for the purposes of also being committed to upstream.")
        sys.exit(1)
    if staged_paths.game_files_changed:
        if not tests.run() == 0:
            sys.exit(1)
    if staged_paths.automation_code_changed:
        if not script_tests.run():
            sys.exit(1)
    with open(os.path.join('automation','post_commit.json'),mode='w') as what_changed:
            what_changed.write(staged_paths.dump())

if __name__ == "__main__":
    run()
