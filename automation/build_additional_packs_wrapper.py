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
import glob
import shutil

temp_filepath = os.path.join('automation',"files_for_pack.txt")

class PacksToBuild:
    list_of_packs = []

    def __init__(self):
        list_of_packs = []

    def copy_build_info_from_config_info(self,config_info_obj):
        for build_inf in config_info_obj.all_build_objects:
            if build_inf.build_type != "asset_pack":
                continue
            pack_to_build = AssetPackBuildInfo()
            pack_to_build.copy_from_other_struct(build_inf)
            self.list_of_packs.append(pack_to_build)


class AssetPackBuildInfo:
    build_dir = ""
    pack_name = ""
    itch_channel_name = ""
    files_included : list = []
    _add_globs : list = []
    _remove_globs : list = []
    add_to_all_platform_packs : bool = True

    def copy_from_other_struct(self,other_build_info) -> None:
        for glob_to_add in other_build_info.add_globs:
            self.add_glob_to_include(glob_to_add)
        for glob_to_remove in other_build_info.remove_globs:
            self.add_glob_to_exclude(glob_to_remove)
        self.itch_channel_name = other_build_info.itch_channel_name
        self.build_dir = other_build_info.build_dir
        self.pack_name = other_build_info.pack_name
        self.add_to_all_platform_packs = other_build_info.add_to_all_platform_packs

    def add_glob_to_include(self,path_to_expand:str) -> None:
        self._add_globs.append(path_to_expand)

    def add_glob_to_exclude(self,path_to_expand:str) -> None:
        self._remove_globs.append(path_to_expand)

    def create_temp_file_with_list_of_files_to_pack(self):
        with open(temp_filepath,'r') as temp_file:
            temp_file.write_line("pack_path " + self.build_dir + '/' + self.pack_name + '.pck\n')
            for filename in self.files_included:
                importfile_path = filename + ".import"
                if os.path.exists(importfile_path):
                    temp_file.write_line(self.resolve_import_file_to_actual_resource_file(
                            importfile_path)+'\n')
                    temp_file.write_line('res://' + importfile_path + '\n')
                else:
                    temp_file.write_line('res://' + filename + '\n')

    def clean_up_temp_file(self) -> None:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

    def resolve_import_file_to_actual_resource_file(self,import_file_path):
        with open(import_file_path,"r") as opened_import_file:
            for line in opened_import_file:
                if line[:6] == 'path="':
                    return line[6:-2]
        return ""

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

    def invoke(self,config) -> None:
        self.create_temp_file_with_list_of_files_to_pack()
        subprocess.run(["godot","-s","../automation/build_additional_packs.gd","--path","game/","--no-window"])
        self.clean_up_temp_file()

def invoke_all(config) -> list:
    packs = PacksToBuild()
    packs.copy_build_info_from_config_info(config)
    for pack in packs.list_of_packs:
        pack.invoke(config)
    # This script is not responsible for copying packs to build directories. Do that in build_game (meaning this one has to be called first).
    return packs.list_of_packs

def copy_pack_to_platform_build_dir_simple_case(pack,build_dir) -> None:
    pack_path = os.path.join("game",pack.build_dir,pack.pack_name + ".pck")
    shutil.copyfile(pack_path,os.path.join(build_dir,pack_name + ".pck"))

def copy_pack_to_platform_build_macos(pack,build_dir) -> None:
    # requires unzipping the .app bundle, copying pack to Contents/Resources, and rezipping
    # TODO: implement
    pass

def copy_pack_to_platform_build_android(pack,build_dir) -> None:
    # requires unzipping the .apk package, copying pack to (where?), editing the manifest, and rezipping
    # TODO: implement
    pass


