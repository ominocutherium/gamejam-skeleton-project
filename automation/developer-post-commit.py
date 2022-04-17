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
import json

sys.path.append(os.getcwd())

import automation.build_docs as builddocs
import automation.build_game as buildgame
import automation.install as install
import automation.upload_builds_to_itch as itchscript
import automation.read_config_file as readconf

conf = readconf.ConfigFileInfo()
conf.read_config()

flags_from_pre_commit = {}
with open(os.path.join('automation','post_commit.json'),mode='r') as p_commit:
    flags_from_pre_commit = json.load(p_commit)
if flags_from_pre_commit["game_files_changed"] or flags_from_pre_commit["assets_changed"]:
    list_of_builds = buildgame.run(conf)
    # TODO: add asset pack builds as well
    itchupload = itchscript.BuildsToUpload(list_of_builds)
    if itchupload.builds_by_platform:
        itchupload.read_itch_user_info_from_config(conf)
        itchupload.push_builds()

if flags_from_pre_commit["docs_changed"]:
    builddocs.run(conf)
if flags_from_pre_commit["automation_code_changed"]:
    # TODO: only install if user is configured as a developer.
    install.run()


os.remove(os.path.join('automation','post_commit.json'))

