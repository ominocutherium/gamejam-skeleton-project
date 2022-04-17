#!/usr/bin/env -S godot -s

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
	if pack_path == "":
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
	return ""


func add_lines_from_opened_file_to_pck(opened_file:File,packer:PCKPacker) -> void:
	pass

