#!/usr/bin/env python3

# Part of ominocutherium's godot gamejam skeleton project.

import unittest

import automation.tests.test_build_docs
import automation.tests.test_install
import automation.tests.test_verify_code_quality
import automation.tests.test_build_game
import automation.tests.test_verify_paths
import automation.tests.test_upload_builds

def run():
    for testcase in [
            automation.tests.test_build_docs,
            automation.tests.test_install,
            automation.tests.test_verify_code_quality,
            automation.tests.test_verify_paths,
            automation.tests.test_build_game,
            automation.tests.test_upload_builds,
            ]:
        tp = unittest.main(module=testcase,exit=False)
        if tp.result.failures or tp.result.errors:
            return False
    return True

