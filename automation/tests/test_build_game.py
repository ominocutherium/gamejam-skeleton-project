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

import unittest
from unittest import mock

import automation.build_game

class BuildModuleTestCase(unittest.TestCase):
    @mock.patch('automation.build_game.sys.exit')
    @mock.patch('automation.build_game.BuildsToBuild')
    def test_run(self,build_game_obj_mock,exit_mock) -> None:
        config_mock = mock.MagicMock()
        build_game_inst_mock = build_game_obj_mock.return_value
        build_game_inst_mock.builds_by_platform = [None,None,None]
        build_game_inst_mock.create_builds.return_value = 0
        return_list = automation.build_game.run(config_mock)
        exit_mock.assert_not_called()
        self.assertIsInstance(return_list,list)
        build_game_obj_mock.assert_called()
        build_game_inst_mock.copy_build_info_from_config_info.assert_called()
        build_game_inst_mock.create_export_presets.assert_called()
        build_game_inst_mock.create_builds.assert_called()

        build_game_inst_mock.create_builds.return_value = 1
        automation.build_game.run(config_mock)
        exit_mock.assert_called()

class BuildsObjTestCase(unittest.TestCase):
#    @mock.patch('automation.build_game.os.path.join')
#    @mock.patch('automation.build_game.os.path.exists')
#    @mock.patch('automation.build_game.BuildInfo')
#    def test_read_build_info(self, build_inf_mock, exists_mock, join_mock) -> None:
#        m = mock.mock_open(read_data="docs_defaults docs.yaml\n\nexport_include game_state/*.gd\nexport_exclude */demo.gd\nbuild_platform html5 exports/game_html5/ HTML5\nexport_include html5_specific/*.tscn\nbuild_platform linux exports/game_linux/ Linux/X11\nbuild_platform macosx exports/game_macosx Mac OSX\n")
#        btb_inst = automation.build_game.BuildsToBuild()
#        btb_inst.builds_by_platform = []
#        with mock.patch('automation.build_game.open',m) as file_mock:
#            btb_inst.read_build_info_from_config()
#        self.assertEqual(len(btb_inst.builds_by_platform),3)
#        default_build_obj_mock = None
#        # TODO: configure side_effect for the BuildInfo mock to have different return values for each call
#        if len(btb_inst.builds_by_platform) > 0:
#            btb_inst.builds_by_platform[0].add_glob_to_include.assert_called_with("html5_specific/*.tscn")
#            self.assertEqual(btb_inst.builds_by_platform[0].itch_channel_name,"macosx")
#            self.assertEqual(btb_inst.builds_by_platform[0].build_dir,"exports/game_macosx")
#            self.assertEqual(btb_inst.builds_by_platform[0].platform_template_name,"Mac OSX")
#        for build_obj_mock in btb_inst.builds_by_platform:
#            build_obj_mock.copy_filesinc_from_other.assert_called()
#            self.assertTrue(build_obj_mock.platform_template_name)
#            self.assertTrue(build_obj_mock.itch_channel_name)
#            self.assertTrue(build_obj_mock.build_dir)

    @mock.patch('automation.build_game.BuildInfo')
    def test_copy_build_info_from_config_info(self,build_inf_mock):
        config_mock = mock.MagicMock()
        btb_inst = automation.build_game.BuildsToBuild()
        config_mock.default_build_info_object = None
        config_mock.all_build_objects = []
        self.assertIsNone(btb_inst.copy_build_info_from_config_info(config_mock))
        self.assertEqual(len(btb_inst.builds_by_platform),0)

        config_mock.all_build_objects = [
                mock.MagicMock(),
                mock.MagicMock(),
                mock.MagicMock(),
        ]
        config_mock.all_build_objects[0].build_type = "platform"
        config_mock.all_build_objects[2].build_type = "default"
        config_mock.all_build_objects[1].build_type = "asset_pack"
        build_inf_instance = build_inf_mock.return_value
        config_mock.default_build_info_object = config_mock.all_build_objects[2]

        self.assertIs(btb_inst.copy_build_info_from_config_info(config_mock),build_inf_instance)
        self.assertEqual(len(btb_inst.builds_by_platform),1)
        build_inf_instance.copy_from_other_struct.assert_called()
        build_inf_instance.copy_filesinc_from_other.assert_called()

    @mock.patch('automation.build_game.os.chdir')
    def test_process_all_globs(self, chdir_mock) -> None:
        btb_inst = automation.build_game.BuildsToBuild()
        btb_inst.builds_by_platform = [mock.MagicMock(),mock.MagicMock(),mock.MagicMock()]
        btb_inst.process_all_globs()
        chdir_mock.assert_any_call('game/')
        chdir_mock.assert_called_with('..')
        for build_mock in btb_inst.builds_by_platform:
            build_mock.process_globs.assert_called()

    def test_get_lines_from_existing_preset(self) -> None:
        btb_inst = automation.build_game.BuildsToBuild()
        btb_inst.builds_by_platform = [mock.MagicMock(),mock.MagicMock(),mock.MagicMock()]
        for i in range(3):
            btb_inst.builds_by_platform[i].platform_template_name = ["temp1","booger","temp0"][i]
            btb_inst.builds_by_platform[i].get_line_of_files_for_export_template.return_value = "line replaced with this\n"
        m = mock.mock_open(read_data="[preset.0]\n\nname=\"temp0\"\nignoreme=true\nexport_files=PoolStringArray(\"thing.gd\"])\n\n[preset.0.options]\nimanoption=true\n\n[preset.1]\n\nname=\"temp1\"\nignoreme=false\nexport_files=PoolStringArray([\"im_being_manually_exported.tscn\"])\n\n[preset.1.options]\nimadifferentoption=false\n")
        lines_returned = []
        with mock.patch('automation.build_game.open',m) as open_mock:
            lines_returned = btb_inst.get_lines_from_existing_preset_file()
        self.assertIn("ignoreme=true\n",lines_returned)
        self.assertNotIn('export_files=PoolStringArray("thing.gd"])',lines_returned)
        self.assertIn("line replaced with this\n",lines_returned)
        btb_inst.builds_by_platform[0].get_line_of_files_for_export_template.assert_called()
        btb_inst.builds_by_platform[1].get_line_of_files_for_export_template.assert_not_called()
        btb_inst.builds_by_platform[2].get_line_of_files_for_export_template.assert_called()

    @mock.patch('automation.build_game.BuildsToBuild.get_lines_from_existing_preset_file')
    @mock.patch('automation.build_game.BuildsToBuild.process_all_globs')
    def test_create_export_presets(self,process_globs_mock,get_lines_mock) -> None:
        lines_list = ['booger0\n','booger1\n','booger2\n']
        get_lines_mock.return_value = lines_list
        btb_inst = automation.build_game.BuildsToBuild()
        m = mock.mock_open()
        with mock.patch('automation.build_game.open',m) as presets_write:
            btb_inst.create_export_presets()
        m().write.assert_any_call(lines_list[0])
        process_globs_mock.assert_called()
        get_lines_mock.assert_called()

    def test_create_builds(self) -> None:
        btb_inst = automation.build_game.BuildsToBuild()
        btb_inst.builds_by_platform = [mock.MagicMock(),mock.MagicMock(),mock.MagicMock()]
        sp_state_mock0 = mock.MagicMock()
        sp_state_mock0.returncode = 0
        sp_state_mock1 = mock.MagicMock()
        sp_state_mock1.returncode = 1
        for buildinfo_mock in btb_inst.builds_by_platform:
            buildinfo_mock.create_build.return_value = sp_state_mock0
        self.assertEqual(btb_inst.create_builds(),0)
        for buildinfo_mock in btb_inst.builds_by_platform:
            buildinfo_mock.create_build.assert_called()
        btb_inst.builds_by_platform[1].create_build.return_value = sp_state_mock1
        self.assertEqual(btb_inst.create_builds(),1)

class BuildInfoTestCase(unittest.TestCase):
    def test_copy_filesinc(self) -> None:
        other_build_inf_mock = mock.MagicMock()
        other_build_inf_mock._add_globs = ["glob1","glob2","glob3"]
        other_build_inf_mock._remove_globs = ["glob0","glob4","glob5"]
        build_inf_instance = automation.build_game.BuildInfo()
        build_inf_instance.copy_filesinc_from_other(other_build_inf_mock)
        self.assertEqual(other_build_inf_mock._add_globs,build_inf_instance._add_globs)
        self.assertIsNot(other_build_inf_mock._add_globs,build_inf_instance._add_globs)
        self.assertEqual(other_build_inf_mock._remove_globs,build_inf_instance._remove_globs)
        self.assertIsNot(other_build_inf_mock._remove_globs,build_inf_instance._remove_globs)

    def test_add_glob_inc(self) -> None:
        new_glob = "newglob0"
        build_inf_instance = automation.build_game.BuildInfo()
        build_inf_instance._add_globs = ["glob0","glob1","glob2"]
        self.assertNotIn(new_glob,build_inf_instance._add_globs)
        build_inf_instance.add_glob_to_include(new_glob)
        self.assertIn(new_glob,build_inf_instance._add_globs)

    def test_add_glob_exc(self) -> None:
        new_glob = "newglob0"
        build_inf_instance = automation.build_game.BuildInfo()
        build_inf_instance._remove_globs = ["glob0","glob1","glob2"]
        self.assertNotIn(new_glob,build_inf_instance._remove_globs)
        build_inf_instance.add_glob_to_exclude(new_glob)
        self.assertIn(new_glob,build_inf_instance._remove_globs)

    @mock.patch('automation.build_game.BuildInfo._add_files_included_from_glob')
    @mock.patch('automation.build_game.BuildInfo._remove_files_included_from_glob')
    def test_process_globs(self, rem_file_mock, add_file_mock) -> None:
        build_inf_instance = automation.build_game.BuildInfo()
        build_inf_instance._add_globs = ["glob1","glob2"]
        build_inf_instance._remove_globs = ["glob1","glob2"]
        build_inf_instance.process_globs()
        add_file_mock.assert_any_call('glob1')
        add_file_mock.assert_any_call('glob2')
        rem_file_mock.assert_any_call('glob1')
        rem_file_mock.assert_any_call('glob2')

    @mock.patch('automation.build_game.glob.glob')
    def test_add_files_inc(self,glob_mock) -> None:
        build_inf_instance = automation.build_game.BuildInfo()
        glob_mock.return_value = ["path0","path1","path2","path3"]
        build_inf_instance._add_files_included_from_glob("glob0")
        self.assertIn("path0",build_inf_instance.files_included)
        glob_mock.return_value = ["path4","path1","path5"]
        build_inf_instance._add_files_included_from_glob("glob1")
        self.assertIn("path4",build_inf_instance.files_included)
        self.assertEqual(build_inf_instance.files_included.count("path1"),1)

    @mock.patch('automation.build_game.glob.glob')
    def test_remove_files_inc(self,glob_mock) -> None:
        build_inf_instance = automation.build_game.BuildInfo()
        build_inf_instance.files_included = ["path0","path1","path2","path3","path4","path5"]
        glob_mock.return_value = ["path6","path3"]
        build_inf_instance._remove_files_included_from_glob("glob0")
        self.assertNotIn("path3",build_inf_instance.files_included)

    @mock.patch('automation.build_game.BuildInfo._get_game_local_files_to_include')
    def test_get_line_of_files(self,list_of_filepaths_mock) -> None:
        list_of_filepaths_mock.return_value = ["res://icon.png","res://Game.tscn","res://Game.gd","res://MainMenu.tscn","res://MainMenu.gd"]
        build_inf_instance = automation.build_game.BuildInfo()
        self.assertEqual(build_inf_instance.get_line_of_files_for_export_template(),'export_files=PoolStringArray( "res://icon.png", "res://Game.tscn", "res://Game.gd", "res://MainMenu.tscn", "res://MainMenu.gd" )\n')

    @unittest.skip('Pending test implementation')
    def test_get_game_local_files(self) -> None:
        self.assertTrue(False)

    @unittest.skip('Pending test implementation')
    def test_create_build(self) -> None:
        self.assertTrue(False)


