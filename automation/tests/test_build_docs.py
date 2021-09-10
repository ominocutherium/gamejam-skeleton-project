#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import unittest
from unittest import mock

import automation.build_docs

class BuildDocsTestCase(unittest.TestCase):
    @mock.patch('automation.build_docs.DocsState')
    def test_run(self,docs_state_mock):
        docs_state_inst_mock = docs_state_mock.return_value
        automation.build_docs.run()
        docs_state_inst_mock.get_defaults_from_config.assert_called()
        docs_state_inst_mock.compile_all_docs.assert_called()

    @mock.patch('automation.build_docs.os.path.exists')
    @mock.patch('automation.build_docs.os.path.join')
    def test_docs_state_get_defaults(self,join_mock,exists_mock):
        # ds_mock = ds_class_mock.return_value
        m = mock.mock_open(read_data='booger booger\ndocs_defaults booger.yaml\ndocs_defaults other.yaml\n')
        ds = automation.build_docs.DocsState()
        with mock.patch('automation.build_docs.open',m):
            ds.get_defaults_from_config()
        self.assertEqual(len(ds.docs_default_files),2)
        self.assertTrue(ds.docs_default_files[0].startswith('booger'))
        
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
