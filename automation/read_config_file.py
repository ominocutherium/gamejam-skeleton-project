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


class ConfigFileInfo:
    docs_default_files = []
    all_build_objects = []
    additional_packages_to_build = []
    default_build_info_object = None
    __current_build_info_object = None
    itch_user = ""
    itch_game_name = ""
    gut_test_dirs = []
    git_primary_branch_name = ""
    

    def __handle_docs_defaults_line(self,line:str):
        self.docs_default_files.append(line.split()[1])

    def __handle_export_exclude_line(self,line:str):
        if self.__current_build_info_object != None:
            self.__current_build_info_object.remove_globs.append(line[:-1].split(None,1)[1])

    def __handle_export_include_line(self,line:str):
        if self.__current_build_info_object != None:
            self.__current_build_info_object.add_globs.append(line[:-1].split(None,1)[1])

    def __handle_build_info_line(self,line:str):
        data = line[:-1].split(None,3)
        if data[3] == "assets":
            self.__current_build_info_object = AssetPackBuildInfo()
        else:
            self.__current_build_info_object = PlatformBuildInfo()
            self.__current_build_info_object.platform_template_name = data[3]
        self.all_build_objects = self.__current_build_info_object
        self.__current_build_info_object.itch_channel_name = data[1]
        self.__current_build_info_object.build_dir = data[2]

    def __handle_itch_config_line(self,line:str):
        data = line[:-1].split()
        if len(data) > 2:
            self.itch_user = data[1]
            self.itch_game_name = data[2]

    def __handle_test_dir_line(self,line:str):
        self.gut_test_dirs.append(line[:-1].split()[1])

    def __handle_git_primary_branch_name(self,line:str):
        self.git_primary_branch_name = line[:-1].split()[1]

    handlers_for_keys = {
            "docs_defaults":__handle_docs_defaults_line,
            "export_include":__handle_export_include_line,
            "export_exclude":__handle_export_exclude_line,
            "build_info":__handle_build_info_line,
            "itch_config":__handle_itch_config_line,
            "git_primary_branchname":__handle_git_primary_branch_name,
            "test_dir":__handle_test_dir_line,
            }

    def __init__(self):
        self.docs_default_files = []
        self.additional_packages_to_build = []
        self.__current_build_info_object = DefaultBuildInfo()
        self.all_build_objects = [self.__current_build_info_object]
        self.gut_test_dirs = []

    def read_config(self):
        if os.path.exists(os.path.join('automation','config.txt')):
            with open(os.path.join('automation','config.txt')) as config_file:
                for line in config_file:
                    line_without_newline = line[:-1]
                    split_line = line_without_newline.split()
                    if len(split_line) > 1 and split_line[0] in self.handlers_for_keys:
                        self.handlers_for_keys[split_line[0]](self,line)

class BuildInfo():
    # have all of the state but none of the behavior of build_game.BuildInfo
    # in build_game, BuildInfo copies from this BuildInfo on initialization
    build_dir = ""
    build_type = ""
    platform_template_name = "" # only for game exports, not asset packs
    itch_channel_name = ""
    files_included : list = []
    add_globs : list = []
    remove_globs : list = []


class PlatformBuildInfo(BuildInfo):
    build_type = "platform"


class DefaultBuildInfo(BuildInfo):
    build_type = "default"


class AssetPackBuildInfo(BuildInfo):
    # have all of the state but none of the behavior of build_asset_packs.AssetPackBuildInfo
    # in build_asset_packs, AssetPackBuildInfo copies from this BuildInfo on initialization
    build_type = "asset_pack"


def read_config():
    config_info = ConfigFileInfo()
    config_info.read_config()
    return config_info

