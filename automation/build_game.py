#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import os
import sys
import subprocess

class BuildsToBuild:
    builds_by_platform = []

    def read_build_info_from_config(self):
        if os.path.exists(os.path.join('automation','config.txt')):
            with open(os.path.join('automation','config.txt')) as config_file:
                for line in config_file:
                    data = line.split()
                    if len(data) > 3:
                        if data[0] = "build_platform":
                            platform = BuildInfo()
                            platform.build_dir = data[1]
                            platform.platform_template_name = data[2]
                            platform.itch_channel_name = data[3]

    def create_builds(self) -> int:
        for platform in builds_by_platform:
            sp_state = platform.create_build()
            if sp_state.return_code != 0:
                return sp_state.return_code
        return 0

class BuildInfo:
    build_dir = ""
    platform_template_name = ""
    itch_channel_name = ""

    def create_build(self):
        sp_state = subprocess.run(["godot","--path","game/","--export",self.platform_template_name])
        return sp_state

def run() -> list:
    builds = BuildsToBuild()
    builds.read_build_info_from_config()
    builds_status = builds.create_builds():
    if builds_status != 0:
        sys.exit(builds_status)
    return builds.builds_by_platform
