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

