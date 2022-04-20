#!/usr/bin/env -S godot -s

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

extends SceneTree

const PATH_OF_TEMP_FILE = "../automation/files_for_pack.txt"


func _init() -> void:
	var f := File.new()

	start_pack_job(f)

	if f.is_open():
		f.close()
	quit()

func start_pack_job(f:File) -> void:
	if !f.file_exists(PATH_OF_TEMP_FILE):
		print("Temp file doesn't exist. Aborting.")
		return
	var err = f.open(PATH_OF_TEMP_FILE,File.READ)
	if err != OK:
		print("Error opening temp file code {0}".format([err]))
		return
	var pack_path := scan_temp_file_for_pack_path(f)
	if pack_path == "" or not pack_path.starts_with('res://'):
		print("Couldn't extract pack path from temp file. Aborting.")
		return
	var packer := PCKPacker.new()
	err = packer.pck_start(pack_path)
	if err != OK:
		print("Error starting the packer for pack path {0}, code {1}".format([pack_path,err]))
		return

	add_lines_from_opened_file_to_pck(f,packer)

	err = packer.flush(true)
	if err != OK:
		print("Error flushing the pack, code {0}".format([err]))
		return
	return


func scan_temp_file_for_pack_path(opened_file:File) -> String:
	var line : String = ""
	while not opened_file.eof_reached():
		line = opened_file.get_line()
		if line.starts_with('pack_path '):
			return 'res://' + line.substr(10)
	return ""


func add_lines_from_opened_file_to_pck(opened_file:File,packer:PCKPacker) -> void:
	var line : String = ""
	while not opened_file.eof_reached():
		line = opened_file.get_line()
		if line != "" and File.file_exists(line):
			packer.add_file(line)

