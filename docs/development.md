# Development

## Setup

### Tools

* [Git](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/)
* Python 3 w/ pip and friends (see section below)
* GNU gettext
* Docker and Docker Compose (optional)
* Travis Tool (optional)

### Configuring Git

If using CLI (not some GUI app):
```
git config --global core.autocrlf false
git config --global user.name <username>
git config --global user.email <email-address>
```

Alternatively, on Windows, use the GitHub for Windows app to setup everything

### Installing Python 2 Virtualenv

Download and install Python 3 and Python 3 pip.

Note: Windows may call Python 3 `python` while Linux typically calls it `python3`.

```
# Linux
sudo pip3 install --upgrade pip virtualenv setuptools wheel
# Windows
py -3 -m pip install --upgrade pip virtualenv setuptools wheel
```

### Installing GNU gettext

Linux: `apt install gettext`

Windows: TODO

### (Optional) Installing and Configuring Docker

Install both Docker and Docker Compose (combined app on Windows).
On Linux, add yourself to the `docker` group and then re-log, so that you can run Docker commands as non-root.

### (Optional) Installing Travis Tool

Optional, used for encrypting Travis CI secrets and files and stuff.
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

## Running

### Run with Virtualenv

This is the intended way to run the app and most scripts in `manage/`. Run `manage/setup.sh` (to setup the virtual environment, add the temporary settings file, migrate the Django DB, add an admin user, etc.). The username and password of the added admin user is "batman" and "manbat". The DB file and log files are located in `.local/venv/`. The local settings file is located at `src/settings/local.py`.

### Tools

Most of these use venv and therefore requires `manage/setup.sh` to be run first (once).

* Cleanup some unimportant local files (Python caches, logs, ...): `manage/clean-lightly.py`
* Cleanup all local files (DB, config, Python caches, logs, ...): `manage/clean-all.py`
* Run linter (check source formatting): `manage/lint.py`
* Run tests: `manage/test.py`
* Run some checks (like the linter, tests, some validation): `manage/check.py`
* Make migrations (after model changes): `manage/make-migrations.py`
* Make translations (updates `locale/nb/django.po`): `manage/make-translations.py`

### Upgrading Dependencies

* This project uses pip-tools with all-dep pinning.
* Run `manage/update-deps.sh` to update dependencies.
* Go through all dep updates (as shown in by the script or git diff), read the changelogs for the changes, and make sure they don't mess things up.

### Run with Docker

This way is intended just for testing Docker stuff.

* Setup: `manage/docker/setup.sh` (first time or after project change)
* Run server: `manage/docker/run.sh`

## Making Changes

* If you're committing code changes, run `manage/check.sh` first to make sure the formatting is correct and that tests still pass.
* If you're adding/changing/fixing features, add it to the changelog.
