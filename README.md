# Battlefield 1942 Build

Invokable CLI tasks for building a Battlefield 1942 mod.

## Prerequisites

#### Debian Linux
```bash
pip install -r requirements.txt
```

#### MacOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

#### Including in a mod git repository

`git submodule add git@github.com:HDN1942/bf1942-build.git tasks`

`inv --list`

## License

Released under GPL-3.0 license unless specified otherwise in source file.