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
import unittest
from unittest import mock

import automation.upload_builds_to_itch

class UploadBuildsTestCase(unittest.TestCase):
    @mock.patch('automation.upload_builds_to_itch.os.path.exists')
    @mock.patch('automation.upload_builds_to_itch.os.path.join')
    def test_read_user_info(self, join_mock, exists_mock):
        m = mock.mock_open(read_data='docs_defaults thing.yaml\nbuild_platform HTML5 html5 exports/my_game_name_html5/\nitch_config myusername my_game_name\nbooger\n')
        btu_instance = automation.upload_builds_to_itch.BuildsToUpload()
        with mock.patch('automation.upload_builds_to_itch.open',m):
            btu_instance.read_itch_user_info_from_config()
        self.assertEqual(btu_instance.itch_user,"myusername")
        self.assertEqual(btu_instance.game_name,"my_game_name")

    @mock.patch('automation.upload_builds_to_itch.subprocess.run')
    def test_push_builds(self,sub_run_mock):
        sub_run_mock.return_value = mock.MagicMock()
        sub_run_mock.return_value.returncode = 0
        build_inf_mock = mock.MagicMock()
        build_inf_mock.itch_channel_name = ""
        build_inf_mock.build_dir = ""
        btu_instance = automation.upload_builds_to_itch.BuildsToUpload()
        btu_instance.builds_by_platform = [build_inf_mock]
        self.assertEqual(btu_instance.push_builds(),0) # exit at guard clause
        sub_run_mock.assert_not_called()
        btu_instance.itch_user = "myusername"
        btu_instance.game_name = "my_game_name"
        self.assertEqual(btu_instance.push_builds(),0) # skip at continue
        sub_run_mock.assert_not_called()
        build_inf_mock.build_dir = "exports/my_game_name_html5/"
        build_inf_mock.itch_channel_name = "html5"
        self.assertEqual(btu_instance.push_builds(),0) # call subprocess
        sub_run_mock.assert_called_with(["butler","push","game/exports/my_game_name_html5/","myusername/my_game_name:html5"])
        sub_run_mock.return_value.returncode = 1
        self.assertEqual(btu_instance.push_builds(),1) # call subprocess, bad return code
