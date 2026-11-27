# TIOJ Problem Tools
**The project is not well tested. Issues or pull requests are welcome to improve us.**

tioj-problem-tools is a python tool for assisting [TIOJ INFOR Online Judge](https://github.com/TIOJ-INFOR-Online-Judge/tioj) problem setting.

By using a specific format base on [Task Preparation System](https://github.com/ioi-2017/tps), problem setters can obtain a command-line interface to conveniently set up problems and then upload them onto a TIOJ-format online judge.

To be short, tioj-problem-tools parses TPS-format problem directories and uses the front-end interface to interact with TIOJ. To deal with custom TIOJ-format, tioj-problem-tools also provides [toml](https://toml.io/en/) configuration files and [JSON schema](https://json-schema.org/understanding-json-schema/index.html) for users to customize their formats.

## Prerequisites

Use Python 3.11 or newer. From the repository root, create a virtual environment and install
runtime dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. The legacy
`python -m pip install -r requirement.txt` command also works from the repository root.

## Usage

Copy the example configuration and edit `configs/default_settings.toml` with your TIOJ URL
and username. Leave the password blank to enter it interactively (the URL and username may
also be left blank for prompts).

```bash
cp -r configs.example configs
python tioj.py --help
```

`configs/` is local and ignored by Git. To work with multiple TIOJ instances, make another
copy and specify its directory with the existing `CONFIGS_DIR` environment variable:

```bash
cp -r configs.example configs-local
# Edit configs-local/default_settings.toml and any instance-specific settings.
CONFIGS_DIR=configs-local python tioj.py whoami
```

Directories named `configs-*` at the repository root are also ignored. For a configuration
outside the repository, set `CONFIGS_DIR` to its absolute path.

**Upgrading an existing checkout:** Before updating, back up your existing `configs/` directory
outside the repository, including any local changes. Git may refuse to update if tracked
configuration files have local edits; after verifying the backup, restore the tracked files
before updating. The previously tracked configuration files are now provided in
`configs.example/`. After updating, copy the new examples into your local `configs/` directory
and transfer your local values and customizations from the backup. Do not overwrite new
configuration keys with an old copy of the entire directory.

Since this tool uses Typer, you can also use Typer CLI (for example, `typer tioj.py`).

## Features

### Upload only the parts you changed

`upload-problem` uploads everything by default. Passing `--update-*` uploads only the parts you
name, while passing `--no-update-*` uploads everything but those, which is an effective speed up
when the testcases are unchanged.

### Prettify command line interface

With the help of [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/en/stable/introduction.html), tioj-problem-tools has a pretty interface. Make users have a comfortable experience.

### JSON verification via JSON schema

tioj-problem-tools use the [python implementation](https://python-jsonschema.readthedocs.io/en/stable/) of [JSON schema](https://json-schema.org/understanding-json-schema/index.html) to set up proper verificatifor the json files in tps directories. Users can also modify the schema to fit their requirements.

### Choose whether to use public samples

Sample paths are configurable in `configs/path_settings.toml`: `sample` defaults to `tests/0-*`
and `public_sample` defaults to `public/examples/*`. By default, problems with a grader use
`public_sample`, and other problems use `sample`. To override this per problem, set
`use_public_sample` in `problem.json` to `true` for `public_sample` or `false` for `sample`.
This does not change the testdata path.

```json
{ "code": "apple", "use_public_sample": true }
```

### Reset a problem without losing its number

Deleting a problem on TIOJ frees its number for reuse by an unrelated problem. `delete-problem`
instead strips a problem back to the state of a freshly created empty one, so a retired number
stays yours and can be filled in again later by `upload-problem`.

### Neat config files

The `configs.example/` directory provides the default TOML settings and JSON schemas. Users customize their local `configs/` directory (or the directory named by `CONFIGS_DIR`) without modifying the tracked examples.

### Edit the tags without knowing what is already there

`upload-problem` writes the whole `tag_list` from `problem.json`, which makes it awkward to
touch one tag on a problem that is tagged on TIOJ but not in its directory. `update-tag` reads
the current tags back first and edits them in place, so adding one keeps the rest.
```
python tioj.py update-tag 1234 dp graph      # add two tags
python tioj.py update-tag 1234 dp --remove   # drop one
python tioj.py update-tag 1234 dp --clear    # replace everything with dp
python tioj.py update-tag 1234 --clear       # no tags at all
```
Pass `--solution` to edit the solution tags instead. A single argument may hold several tags
separated by commas, the way TIOJ itself stores them.

## Development

Install the optional development dependencies in the virtual environment:

```bash
python -m pip install -e '.[dev]'
```

The development tools are configured in `pyproject.toml`:

```bash
ruff check .
ruff format --check .
python -m pytest
python -m pytest --cov=src --cov=tioj --cov-report=term-missing
```

Ruff may report existing style issues until the planned formatting and refactoring work is
complete. Do not run a repository-wide automatic fix as part of an unrelated change.
Tests should use temporary configuration or mocked HTTP interactions rather than a real TIOJ
account. The application is still run from the source checkout; installing the package as a
standalone CLI is planned for a later phase.

## Todolist

- Allow uploading testcases without tps directory format validation.
- Allow "Banned compilers" when editing TIOJ problem's metadata.
- A more comfortable usage for replacing the strings.
- Testing.
- Interactive CLI.
