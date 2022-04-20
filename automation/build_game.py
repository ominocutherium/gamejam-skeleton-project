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
import subprocess
import glob

class BuildsToBuild:
    builds_by_platform = []

    def copy_build_info_from_config_info(self,config_info_obj):
        default_build_info = None
        if config_info_obj.default_build_info_object != None:
            default_build_info = BuildInfo()
            default_build_info.copy_from_other_struct(config_info_obj.default_build_info_object)
        for build_inf in config_info_obj.all_build_objects:
            if build_inf.build_type == "default":
                continue
            elif build_inf.build_type == "platform":
                platform_to_build = BuildInfo()
                platform_to_build.copy_from_other_struct(build_inf)
                self.builds_by_platform.append(platform_to_build)
                if default_build_info != None:
                    platform_to_build.copy_filesinc_from_other(default_build_info)
            # this module doesn't use "asset_pack"
        return default_build_info

    def process_all_globs(self) -> None:
        os.chdir("game/")
        for build_info in self.builds_by_platform:
            build_info.process_globs()
        os.chdir("..")

    def get_lines_from_existing_preset_file(self) -> list:
        lines_to_write = []
        with open('game/export_presets.cfg','r') as export_presets_file:
            build : BuildInfo
            for line in export_presets_file:
                if line.startswith('name='):
                    for build_inf in self.builds_by_platform:
                        if build_inf.platform_template_name == line[6:-2]:
                            build = build_inf
                            break
                if line.startswith('export_files=') and build:
                    lines_to_write.append(build.get_line_of_files_for_export_template())
                else:
                    lines_to_write.append(line)
        return lines_to_write

    def create_export_presets(self) -> None:
        self.process_all_globs()
        lines_to_write = self.get_lines_from_existing_preset_file()
        with open('game/export_presets.cfg','w') as export_presets_file:
            for line_to_write in lines_to_write:
                export_presets_file.write(line_to_write)

    def create_builds(self) -> int:
        for platform in self.builds_by_platform:
            pass
            sp_state = platform.create_build()
            if sp_state.returncode != 0:
                return sp_state.returncode
        return 0

class BuildInfo:
    build_dir = ""
    platform_template_name = ""
    itch_channel_name = ""
    files_included : list = []
    _add_globs : list = []
    _remove_globs : list = []

    def __init__(self):
        files_included = []
        _add_globs = []
        _remove_globs = []

    def copy_from_other_struct(self,other_build_info) -> None:
        for glob_to_add in other_build_info.add_globs:
            self.add_glob_to_include(glob_to_add)
        for glob_to_remove in other_build_info.remove_globs:
            self.add_glob_to_exclude(glob_to_remove)
        self.platform_template_name = other_build_info.platform_template_name
        self.itch_channel_name = other_build_info.itch_channel_name
        self.build_dir = other_build_info.build_dir

    def copy_filesinc_from_other(self,other_build_info) -> None:
        self._add_globs = other_build_info._add_globs.copy()
        self._remove_globs = other_build_info._remove_globs.copy()
        self.files_included = other_build_info.files_included.copy()

    def add_glob_to_include(self,path_to_expand:str) -> None:
        self._add_globs.append(path_to_expand)

    def add_glob_to_exclude(self,path_to_expand:str) -> None:
        self._remove_globs.append(path_to_expand)

    def process_globs(self) -> None:
        for path_to_expand in self._add_globs:
            self._add_files_included_from_glob(path_to_expand)
        for path_to_expand in self._remove_globs:
            self._remove_files_included_from_glob(path_to_expand)

    def _add_files_included_from_glob(self,path_to_expand:str) -> None:
        files_to_append : list = glob.glob(path_to_expand)
        for add_filename in files_to_append:
            if not add_filename in self.files_included:
                self.files_included.append(add_filename)

    def _remove_files_included_from_glob(self,path_to_expand:str) -> None:
        files_to_remove : list = glob.glob(path_to_expand)
        for remove_filename in files_to_remove:
            if remove_filename in self.files_included:
                self.files_included.remove(remove_filename)

    def get_line_of_files_for_export_template(self) -> str:
        return 'export_files=PoolStringArray( "{0}" )\n'.format('", "'.join(self._get_game_local_files_to_include()))

    def _get_game_local_files_to_include(self) -> list:
        local_files = []
        for file in self.files_included:
            local_files.append("res://" + file)
        return local_files

    def create_build(self):
        sp_state = subprocess.run(["godot","--path","game/","--export",self.platform_template_name])
        return sp_state

def run(config) -> list:
    builds = BuildsToBuild()
    builds.copy_build_info_from_config_info(config)
    builds.create_export_presets()
    builds_status = builds.create_builds()
    if builds_status != 0:
        sys.exit(builds_status)
    return builds.builds_by_platform

