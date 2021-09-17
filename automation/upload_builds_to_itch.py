#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import subprocess

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
                    if len(line.split()) > 2:
                        if line.split()[0] == "itch_config":
                            self.itch_user = line.split()[1]
                            self.game_name = line.split()[2]
   
    def push_builds(self) -> int:
        if self.itch_user == "" or self.game_name == "":
            return 0
        for build_info in builds_by_platform:
            sp_status = subprocess.run([
                    "butler",
                    "push",
                    build_info.build_dir,
                    self.itch_user + "/" + self.game_name + ":{0}".format(build_info.itch_channel_name)
                    ])
            if sp_status.return_code != 0:
                return sp_status.return_code
        return 0

# No run function because requires data from another module ('automation/build_game') to work.

