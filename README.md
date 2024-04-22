# Battlefield 1942 Build

Invokable CLI tasks for building a Battlefield 1942 mod.

## Prerequisites

- Python >= 3.10

### Installing Python libraries

#### Windows & Linux
```
pip install -r requirements.txt
```

#### MacOS
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Installation

The build system expects your mod source files to be located in a `src` directory.
See https://github.com/HDN1942/bf1942-fh-sp for a working example.

#### Including in a mod git repository

```
git submodule add git@github.com:HDN1942/bf1942-build.git
git submodule update --init --recursive

inv -r bf1942-build --list
```

Optionally create a symlink to simplify the inv command:

##### Windows

```
mklink /D tasks .\bf1942-build\tasks

inv --list
```

##### Linux / MacOS

```
ln -s ./bf1942-build/tasks tasks

inv --list
```

## Tasks

List of available commands and tasks.
Tasks that have dependencies on other tasks will have their dependencies run before running the task.

Please note that all references to 'mod' refer to the mod configured in invoke.yaml.
Tasks such as install/uninstall will not affect other installed Battlefield 1942 mods.

#### General

List available tasks

`inv --list`

Display help for a specific task

`inv install --help`

#### Build

`inv build`

Performs steps needed to build complete mod, including processing files and packing archives (RFAs).
Only archives that are out-of-date will be built.
Out-of-date in this case means one or more files have been added/changed/deleted since the last build.

Will generate a mod `init.con` file if one does not exist under `src` directory.

##### Processing

###### sound

Sound files not contained in the usual 44khz/22khz/11khz directories are automatically converted to 44/22/11 kHz
wav files and placed in the correct directory structure.

#### Clean

`inv clean`

Deletes temporary build files, effectively marking all archives as out-of-date.

#### Install

`inv install`

Installs (copies) out-of-date mod archives and files into Battlefield 1942 mods directory.

##### Options

- `-f`, `--force`

  Forces installation for all files, including up-to-date ones.

Depends on the build task.

#### Uninstall

`inv uninstall`

Uninstalls (deletes) all built mod archives and files from Battlefield 1942 mods directory.

#### Launch

`inv launch --level Guadalcanal`

Launches a Battlefield 1942 level under the configured mod.

Depends on the install task.

##### Options

- `--no--debug`

  By default the debug exe will be executed, specify `--no-debug` to use the retail exe instead.

- `-g`, `--gpm`

  Set the desired game play mode, the default is GPM_COOP.

- `-l`, `--level`

  Set the level to load, default is the last played level.

- `-m`, `--mod`

  Set the mod to load, default is the configured mod.

## Config

The default config is documented in `invoke.default.yaml`.
This file should be copied to `invoke.yaml` and modified to suit your environment.
At a minimum you should configure the values in the mod section.

## Development

#### Unit tests

`python3 -m unittest`

#### Integration testing

`inv -f ./test/invoke.yaml --list`

## License

Released under GPL-3.0 license unless specified otherwise in source file.