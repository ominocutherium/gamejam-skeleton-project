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

import subprocess
import os

class BuildsToUpload:
    builds_by_platform = []
    itch_user : str = ""
    game_name : str = ""

    def __init__(self,list_of_build_info:list=[]):
        self.builds_by_platform = list_of_build_info

    def read_itch_user_info_from_config(self):
        if os.path.exists(os.path.join('automation','config.txt')):
            with open(os.path.join('automation','config.txt')) as config_file: 
                for line in config_file:
                    if len(line[:-1].split()) > 2:
                        if line[:-1].split()[0] == "itch_config":
                            self.itch_user = line.split()[1]
                            self.game_name = line.split()[2]
   
    def push_builds(self) -> int:
        if self.itch_user == "" or self.game_name == "":
            return 0
        for build_info in self.builds_by_platform:
            if not (build_info.itch_channel_name and build_info.build_dir):
                continue
            sp_status = subprocess.run([
                    "butler",
                    "push",
                    "game/" + build_info.build_dir,
                    self.itch_user + "/" + self.game_name + ":{0}".format(build_info.itch_channel_name)
                    ])
            if sp_status.returncode != 0:
                return sp_status.returncode
        return 0

# No run function because requires data from another module ('automation/build_game') to work.

