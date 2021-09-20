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

import automation.install

class InstallTestCase(unittest.TestCase):
    @mock.patch('automation.install.os.path.exists')
    @mock.patch('automation.install.os.path.join')
    def test_get_role_from_config(self,path_join_mock,path_exists_mock):
        m = mock.mock_open(read_data='booger booger\ndocs_defaults booger.yaml\nrole developer\n')
        ir = automation.install.InstallRole()
        with mock.patch('automation.install.open',m):
            ir.get_role_from_working_tree_config()
            self.assertEqual(ir.role,"developer")
        m2 = mock.mock_open(read_data='booger booger\nbooger booger\n')
        ir2 = automation.install.InstallRole()
        with mock.patch('automation.install.open',m2):
            ir2.get_role_from_working_tree_config()
            self.assertEqual(ir2.role,"fresh")
        path_exists_mock.assert_called()
        path_join_mock.assert_called()

    @unittest.skip("Pending test implementation.")
    def test_write_role(self):
        self.assertTrue(False)

    @unittest.skip("Pending test implementation.")
    def test_install_as_dev(self):
        self.assertTrue(False)

    @unittest.skip("Pending test implementation.")
    def test_clear_dev_install(self):
        self.assertTrue(False)

    @unittest.skip("Pending test implementation.")
    def test_install(self):
        self.assertTrue(False)

    @mock.patch('automation.install.InstallRole')
    def test_run(self,ir_class_mock):
        ir_class_mock.return_value = mock.MagicMock()
        automation.install.run()
        ir_class_mock.return_value.get_role_from_working_tree_config.assert_called()
        ir_class_mock.return_value.install.assert_called()

