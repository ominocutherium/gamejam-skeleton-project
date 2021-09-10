#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import unittest
from unittest import mock

import automation.verify_staged_paths_in_commit

class VerifyStagedPathsTestCase(unittest.TestCase):
    @mock.patch('automation.verify_staged_paths_in_commit.StagedPathsInCommit')
    def test_run(self,sp_class_mock):
        inst_mock = sp_class_mock.return_value
        inst = automation.verify_staged_paths_in_commit.run()
        self.assertEqual(inst_mock,inst)
        inst_mock.query_tree_for_staged_paths.assert_called()
        inst_mock.evaluate_staged_paths.assert_called()

    # I'm not sure this method actually needs a unit test.
    # @mock.patch('automation.verify_staged_paths_in_commit.StagedPathsInCommit')
    # @unittest.skip("Pending test implementation.")
    # def test_sp_declare(self,sp_class_mock):
        # inst_mock = sp_class_mock.return_value
        # self.assertTrue(False)

    @mock.patch('automation.verify_staged_paths_in_commit.json.dumps')
    def test_sp_dump(self,json_dumps_mock):
        dump_return_mock = mock.MagicMock()
        json_dumps_mock.return_value = dump_return_mock
        sp_inst = automation.verify_staged_paths_in_commit.StagedPathsInCommit()
        self.assertEqual(sp_inst.dump(),dump_return_mock)

    @mock.patch('automation.verify_staged_paths_in_commit.subprocess.run')
    def test_sp_query_tree(self,sub_run_mock):
        sub_run_result_mock = mock.MagicMock()
        sub_run_mock.return_value = sub_run_result_mock
        sub_run_result_mock.stdout = mock.MagicMock()
        decoded_mock = mock.MagicMock()
        spltln_mock = mock.MagicMock()
        sub_run_result_mock.stdout.decode = decoded_mock
        decoded_mock.return_value.splitlines = spltln_mock
        spltln_mock.return_value = ["MM path/one","?? path/ignore","MM path/two","  thing"]
        sp_inst = automation.verify_staged_paths_in_commit.StagedPathsInCommit()
        sp_inst.query_tree_for_staged_paths()
        sub_run_mock.assert_called()
        decoded_mock.assert_called()
        spltln_mock.assert_called()
        self.assertEqual(len(sp_inst.paths),2)
        self.assertIn('path/one',sp_inst.paths)
        self.assertNotIn('path/ignore',sp_inst.paths)

    def test_sp_verify_one_not_both(self):
        sp_inst = automation.verify_staged_paths_in_commit.StagedPathsInCommit()
        sp_inst.automation_code_changed = True
        self.assertTrue(sp_inst.verify_only_content_or_automation_changes_staged_not_both())
        sp_inst.automation_code_changed = False
        sp_inst.game_files_changed = True
        self.assertTrue(sp_inst.verify_only_content_or_automation_changes_staged_not_both())
        sp_inst.automation_code_changed = True
        self.assertFalse(sp_inst.verify_only_content_or_automation_changes_staged_not_both())

    def test_sp_evaluate_staged_paths(self):
        sp_inst = automation.verify_staged_paths_in_commit.StagedPathsInCommit()
        sp_inst.paths.append('automation/booger.py')
        sp_inst.evaluate_staged_paths()
        self.assertTrue(sp_inst.automation_code_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('automation/booger.md')
        sp_inst.evaluate_staged_paths()
        self.assertFalse(sp_inst.automation_code_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('docs/booger.md')
        sp_inst.evaluate_staged_paths()
        self.assertTrue(sp_inst.docs_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('docs/booger.png')
        sp_inst.evaluate_staged_paths()
        self.assertFalse(sp_inst.docs_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('website/booger.md')
        sp_inst.evaluate_staged_paths()
        self.assertTrue(sp_inst.website_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('website/booger.html')
        sp_inst.evaluate_staged_paths()
        self.assertFalse(sp_inst.website_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('game/booger.gd')
        sp_inst.evaluate_staged_paths()
        self.assertTrue(sp_inst.game_files_changed)
        self.assertFalse(sp_inst.assets_changed)
        self.reset_sp_inst(sp_inst)
        sp_inst.paths.append('game/booger.tres')
        sp_inst.evaluate_staged_paths()
        self.assertFalse(sp_inst.game_files_changed)
        self.assertTrue(sp_inst.assets_changed)

    def reset_sp_inst(self,sp_inst):
        sp_inst.automation_code_changed = False
        sp_inst.docs_changed = False
        sp_inst.website_changed = False
        sp_inst.assets_changed = False
        sp_inst.game_files_changed = False
        sp_inst.paths = []

