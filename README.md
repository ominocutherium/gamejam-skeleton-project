# Game Jam Skeleton Project

A template project to use for all of my future Godot projects, whether solo or team! I'm also trying to make it robust enough and useful enough for other people to use.

Requires Python 3.5 or later.

## How to Use

If you are starting a new project, see the "Setup" section below.

* If you have an existing game, move the whole game project (minus `README.md` if you have one) to a `game/` subfolder, then copy the entire `automation/` folder from this project into your project folder.
* Run `python automation/install.py` in your terminal.
* If you want to run unit tests for your game scripts, install GUT in your Godot project if it isn't already.
* Ensure you have export presets set up for all of your intended platforms in `game/export_presets.cfg`.
* Edit your config file `automation/config.txt` to match the presets in your export presets file and filters for the files you want to include/exclude in your builds. See "Configuring Builds" below.
* Commit your changes (or setup Git in your project if you have not)

Then you are done! Each time you make changes to your game and commit them to `master`, your project will export automatically.

## New Project Setup

* Create a new repository with this one as a template.
* Highly recommended: install and setup Git LFS in your new repository: `git lfs track *.png`. Do this for all binary filetypes you anticipate using; `*.kra`, `*.psd`, `*.blend`, etc.
* Start the Godot project itself in the `game/` directory. I.e. `project.godot` should be located here: `game/project.godot`. Make sure to immediately set the name of the new project to the game's actual name, so it's not just called "game" in Godot's project list.
* Install GUT through Godot's asset library for unit testing (as well as any other Godot addons you wish to use for your project).
* Lastly, remember to edit your config file `automation/config.txt` (see "Configuring Builds" below), create your export presets (`game/export_presets.cfg`), and overwrite `README.md` with information about your project before committing for the first time.
* After each time you clone your new project, run `automation/install.py` from the command line in the root directory. You will be prompted for a role. Entering the "developer" role will install the automated build scripts to the pre-commit and post-commit hooks. The "artist" role is not yet implemented.

Attempting to run the Godot project without GUT installed will create an error about `addons/gut/test.gd` not existing. I'm still deciding on a remedy for this, whether to include GUT as a subtree in this repository and install it to the godot project automatically, or to use auto-patching to ensure tests are excluded from Artist branches.

## Automated Builds

In the spirit of continuous integration and smooth flow from development to deployment, there are scripts to support re-building and re-uploading the game each time a change has been made. The scripts included in `automation/` are intended for single-coder teams where it may be slightly more efficient for the developer to run the tests and builds on their own computer. This pipeline has many of the features expected of a CI workflow with less complexity and easier security.

The build process only runs in `master` branch, so you can use additional branches for staging purposes without triggering the build. Every time you attempt to commit to master as a developer, the specified tests are run. If all the tests pass, the commit is accepted, and, after the commit completes, the project is exported to all specified platforms (and, if you have Itch.io butler configured, pushed to your Itch.io account, allowing players to access your changes immediately).

Eventually, though it isn't implemented now, I intend to implement the automated builds as Github workflows, too, so that the need to have certain tools installed is removed, and so that builds can be triggered by anyone on the team. But, because this approach does not have the security and simplicity advantage that running the whole process on the developer's own computer does, so the offline build scripts will be maintained as a higher priority.

Additionally, documentation has an automatic build process associated with it. Modular single-heading markdown files can be compiled together into a reader-friendly webpage or ebook through the use of a defaults file, which allows ad hoc addition, removal, or re-ordering of chapters. Example use: an "upcoming features & roadmap" doc and a "implemented features & tutorials" doc are kept up to date at the same time; when a feature becomes implemented, its corresponding doc chapter is moved from "upcoming features" to "features and tutorials" without requiring an entire rewrite. Additionally, for game projects with a narrative, automatic script-compilation tools can bridge the gap between tools writers are familiar with and game assets, allowing for live updating of both a published game script file and the in-game script.

### Configuring Builds

Various build information is stored in `automation/config.txt`, which is intended to be project-dependent and version-tracked. To use, create this file and fill it with the following:

* For each directory of unit tests, make a line with `test_dir` then the path of the directory of GUT tests relative to `game/`, e.g. `test_dir tests/game_mechanics` to run the test scripts located in `game/tests/game_mechanics/`.
* For each document, make a line with `docs_defaults` then the path of the YAML-formatted defaults file to use relative to `docs/`, e.g. `docs_defaults features.yaml` for a defaults file located at `docs/features.yaml`.
* To include files in the export presets, make a line that starts with `export_include` and then a path with wildcards; e.g. `game_state/*.gd`. '*' wildcards are expanded, and paths are relative to `game/`, e.g. if `game_state/*.gd` is specified, then `game/game_state/player_data.gd` will be included as `res://game_state/player_data.gd` in the export preset.
* To exclude files in export presets which would otherwise be included due to a wildcard include pattern, specify them with a line that starts with `export_exclude`. Like includes, these are relative to `game/` and therefore relative to `res://`.
* For each platform to export, make a line with `build_platform` then the following: a one-word, all-lowercase name for the platform (used by butler for the channel name), the export directory for that platform (relative to `game/`), then lastly the name of the platform in the export preset (will likely be `Linux/X11`, `Mac OSX`, `Windows Desktop`, `HTML5`, etc.)
* Any `export_include` and `export_include` lines AFTER the definition of a build platform will apply to the most recently defined platform only (e.g. export some additional Javascript files in the HTML5 build only).
* For Itch uploads, make a line which starts with `itch_config` and include the username of the project creator followed by the game name (must match the game's url). You must configure `butler` with login credentials to have permission to push to this url (automatic if you are the project creator, otherwise have the creator add you as a contributor). `butler` will push all of the builds to channels named as the first argument in the `build_platform` entry for that platform.

Here is an example file:
```
export_include game_state/*
export_include environments/*
export_exclude environments/placeholder_texture.png
test_dir tests/game_mechanics
docs_defaults docs/game_design_doc.md
build_platform html5 exports/my_game_name_html5 HTML5
export_include js/script_only_relevant_to_html5_build.js
build_platform windows exports/my_game_name_win Windows Desktop
itch_config myusername my_game_name
```

Make sure to commit this file in your project. Editing this file is how you make changes to what platforms to build for and what is included in your builds (i.e. it's probably a good idea to exclude unit test files and demo scenes which aren't needed for the release version of your game).

The automation scripts also create and use `automation/working_tree_config.txt` and `automation/post_commit.json` files, which are meant to be install/commit specific and are not version tracked (i.e. keep them in `.gitignore`).

Another file which is necessary for the scripts to work is `game/export_presets.cfg`, which is automatically generated by Godot when setting up exports. While the file is edited automatically, both by Godot itself when using the export dialog and by the build script when including/excluding files, it should be version-tracked in your repository to track changes to the various options (the only lines changed by `automation/build_game.py` are lines starting with `export_filter` and `export_files`; all other lines are copied over). Make sure the exported file uses the same directory specified the `build_platform` line in your config and that it is local to `res://`.

## Additional dependencies required: (Developer Install Only)

* Godot 3.2.x or 3.3.x registered to path as `godot`
* Godot Unit Test (GUT) addon in project in `game/addons/gut/`
* butler by Itch.io (only for uploading to itch.io)
* Pandoc (for compiling markdown docs into other formats)

## Getting Updates

If you made your project by *cloning* this repository, you can use `git fetch` and `git cherry-pick` (do not `pull`) to apply changes from commits to automation scripts.

However, if you used this repository as a template repository, or simply copied the `automation/` directory, you won't be able to cherry-pick because the two projects will not share any common history (this also applies if you rebased your game repository for any reason; I ended up doing this with the initial game projects I made  because I needed to remove all traces of my personal email address). You can instead create and apply patches from diffs.

```
git diff master~1 HEAD > ../script_patch.txt
cd ../MyGameRepository
git apply ../script_patch.txt && git commit -a -m "Patch updates to scripts"
```

## TODO (This repository)

* [x] Implement script which reads `automation/config.txt` and creates export templates; prior to build step
* [x] Implement builds
* [x] Implement automatic pushing to itch
* [ ] Blacklist a set of dates for pushing to itch according to config (for, possibly, Godot Wild Jam in which game updates are not allowed during judging)
* [ ] Implement unit tests for already implemented scripts:
	* [x] build_docs.py
	* [x] build_game.py
	* [ ] developer-pre-commit.py
	* [ ] developer-post-commit.py
	* [x] install.py
	* [ ] verify_code_quality.py
	* [x] verify_staged_paths_in_commit.py
* [x] Hook running of Python unit tests into code verification steps (after ensuring it is an automation script only commit)
* [ ] Make a helper script (not part of the CI process) which automatically creates test files for python scripts (using unittest and unittest.mock) and GDScript classes (using Gut, and reading from project.godot to attempt to set up dependency doubles beforehand)
