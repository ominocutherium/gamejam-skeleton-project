#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import os
import sys
import json

sys.path.append(os.getcwd())

import automation.build_docs as builddocs
import automation.build_game as buildgame
import automation.install as install

flags_from_pre_commit = {}
with open(os.path.join('automation','post_commit.json'),mode='r') as p_commit:
    flags_from_pre_commit = json.load(p_commit)
if flags_from_pre_commit["game_files_changed"] or flags_from_pre_commit["assets_changed"]:
    buildgame.run()
if flags_from_pre_commit["docs_changed"]:
    builddocs.run()
if flags_from_pre_commit["automation_code_changed"]:
    # TODO: only install if user is configured as a developer.
    install.run()


os.remove(os.path.join('automation','post_commit.json'))

