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

import automation.build_docs

class BuildDocsTestCase(unittest.TestCase):
    @mock.patch('automation.build_docs.DocsState')
    def test_run(self,docs_state_mock):
        docs_state_inst_mock = docs_state_mock.return_value
        config_mock = mock.MagicMock()
        automation.build_docs.run(config_mock)
        docs_state_inst_mock.get_defaults_from_config.assert_called()
        docs_state_inst_mock.compile_all_docs.assert_called()

    # @mock.patch('automation.build_docs.os.path.exists')
    # @mock.patch('automation.build_docs.os.path.join')
    # def test_docs_state_get_defaults(self,join_mock,exists_mock):
        # ds_mock = ds_class_mock.return_value
        # m = mock.mock_open(read_data='booger booger\ndocs_defaults booger.yaml\ndocs_defaults other.yaml\n')
        # ds = automation.build_docs.DocsState()
        # with mock.patch('automation.build_docs.open',m):
            # ds.get_defaults_from_config()
        # self.assertEqual(len(ds.docs_default_files),2)
        # self.assertTrue(ds.docs_default_files[0].startswith('booger'))

    def test_docs_state_get_defaults(self):
        config_mock = mock.MagicMock()
        config_mock.docs_default_files = ['def1.yaml','def2.yaml']
        ds = automation.build_docs.DocsState()
        ds.get_defaults_from_config(config_mock)
        self.assertIsNot(ds.docs_default_files,config_mock.docs_default_files)
        for filename in config_mock.docs_default_files:
            self.assertIn(filename,ds.docs_default_files)

        
    @mock.patch('automation.build_docs.os.getcwd')
    @mock.patch('automation.build_docs.os.chdir')
    @mock.patch('automation.build_docs.subprocess.run')
    def test_docs_state_compile(self,subprc_mock,chdir_mock,cwd_mock):
        ds = automation.build_docs.DocsState()
        ds.docs_default_files = ['def1.yaml','def2.yaml']
        ds.compile_all_docs()
        self.assertEqual(subprc_mock.call_count,2)
        self.assertEqual(chdir_mock.call_count,2)
        self.assertEqual(cwd_mock.call_count,1)
