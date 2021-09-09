# Game Jam Skeleton Project

A template project to use for all of my future Godot projects, whether solo or team!

## Setup (Requires Python 3)

Create a new repository with this one as a template.

Highly recommended: install and setup Git LFS in your new repository: `git lfs track *.png`. Do this for all binary filetypes you anticipate using; `*.kra`, `*.psd`, `*.blend`, etc.

Start the Godot project itself in the `game/` directory. I.e. `project.godot` should be located here: `game/project.godot'. Make sure to immediately set the name of the new project to the game's actual name, so it's not just called "game" in Godot's project list.

Install GUT through Godot's asset library for unit testing (as well as any other Godot addons you wish to use for your project).

Lastly, remember to overwrite `README.md` with information about your project.

After each time you clone your new project, run `automation/install.py` from the command line in the root directory. You will be prompted for a role. Entering the "developer" role will install the automated build scripts to the pre-commit and post-commit hooks. The "artist" role is not yet implemented.

Attempting to run the Godot project without GUT installed will create an error about `addons/gut/test.gd` not existing. I'm still deciding on a remedy for this, whether to include GUT as a subtree in this repository and install it to the godot project automatically, or to use auto-patching to ensure tests are excluded from Artist branches.

## Automated Builds

In the spirit of continuous integration and smooth flow from development to deployment, there are scripts to support re-building and re-uploading the game each time a change has been made. The scripts included in `automation/` are intended for single-coder teams where it may be slightly more efficient for the developer to run the tests and builds on their own computer.

The build process only runs in `master` branch, so you can use additional branches for staging purposes without triggering the build. Every time you attempt to commit to master as a developer, the specified tests are run. If all the tests pass, the commit is accepted, and, after the commit completes, the project is exported to all specified platforms (and, if you have Itch.io butler configured, pushed to your Itch.io account, allowing players to access your changes immediately).

Eventually, though it isn't implemented now, I intend to implement the automated builds as Github workflows, too, so that the need to have certain tools installed is removed, and so that builds can be triggered by anyone on the team.

Additionally, documentation has an automatic build process associated with it. Modular single-heading markdown files can be compiled together into a reader-friendly webpage or ebook through the use of a defaults file, which allows ad hoc addition, removal, or re-ordering of chapters. Example use: an "upcoming features & roadmap" doc and a "implemented features & tutorials" doc are kept up to date at the same time; when a feature becomes implemented, its corresponding doc chapter is moved from "upcoming features" to "features and tutorials" without requiring an entire rewrite. Additionally, for game projects with a narrative, automatic script-compilation tools can bridge the gap between tools writers are familiar with and game assets, allowing for live updating of both a published game script file and the in-game script.

### Configuring Builds

Various build information is stored in `automation/config.txt`, which is intended to be project-dependent and version-tracked. To use, create this file and fill it with the following:

* For each directory of unit tests, make a line with `test_dir` then the path of the directory of GUT tests relative to `game/`, e.g. `test_dir tests/game_mechanics` to run the test scripts located in `game/tests/game_mechanics/`.
* For each document, make a line with `docs_defaults` then the path of the YAML-formatted defaults file to use relative to `docs/`, e.g. `docs_defaults features.yaml` for a defaults file located at `docs/features.yaml`.
* For each platform to export, make a line with `platform` then the name of the platform, e.g. `platform html5`.
* To include files in the export templates, make a line that starts with `export_include` and then a path with wildcards; e.g. `game_state/\*.gd`. '*' wildcards are expanded, and paths are relative to `game/`, e.g. if `game_state/\*.gd` is specified, then `game/game_state/player_data.gd` will be included as `res://game_state/player_data.gd` in the export template.
* To exclude files in export templates which would otherwise be included due to a wildcard include pattern, specify them with a line that starts with `export_exclude`. Like includes, these are relative to `game/` and therefore relative to `res://`.
* For Itch uploads, make a line which starts with `itch_user` and then the username of the project creator (must match the game's url). Also, make a second line that starts with `itch_game_name`

Then commit the file.

The automation scripts also create and use `automation/working_tree_config.txt` and `automation/post_commit.txt` files, which are meant to be install/commit specific and are not version tracked (i.e. keep them in `.gitignore`).

## Tools required: (Developer Install Only)

* Godot 3.2.x or 3.3.x registered to path as `godot`
* Godot Unit Test (GUT) addon in project in `game/addons/gut/`
* Coreutils
* Pandoc (for compiling markdown docs into other formats)

## TODO (This repository)

* [ ] Implement script which reads `automation/config.txt` and creates export templates; prior to build step
* [ ] Implement builds
* [ ] Implement automatic pushing to itch
* [ ] Blacklist a set of dates for pushing to itch according to config (for, possibly, Godot Wild Jam in which game updates are not allowed during judging)
* [ ] Implement unit tests for already implemented scripts:
	* [ ] build_docs.py
	* [ ] build_game.py
	* [ ] developer-pre-commit.py
	* [ ] developer-post-commit.py
	* [ ] install.py
	* [ ] verify_code_quality.py
	* [ ] verify_staged_paths_in_commit.py
* [ ] Hook running of Python unit tests into code verification steps (after ensuring it is an automation script only commit)
