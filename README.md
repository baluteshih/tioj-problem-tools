# tioj-problem-tools
**THIS PROJECT IS STILL IN DEVELOPMENT**

tioj-problem-tools is a python tool for assisting [TIOJ INFOR Online Judge](https://github.com/adrien1018/tioj) problem setting.

By using a specific format base on [Task Preparation System](https://github.com/ioi-2017/tps), problem setters can obtain a command-line interface to conveniently set up problems and then upload them onto a TIOJ-format online judge.

To be short, tioj-problem-tools parses TPS-format problem directories and uses the front-end interface to interact with TIOJ. To deal with custom TIOJ-format, tioj-problem-tools also provides json formatters for users to customize their formats.

## Prerequisites

You may need to install the required python packages.
```
pip install "typer[all]" requests bs4 json html_form_to_dict
```

## Usage

Run the script with python.
```
python tioj.py
```

Since this tool is developed by [Typer](https://typer.tiangolo.com/), you can also use [Typer CLI](https://typer.tiangolo.com/typer-cli/) for convenience (like having auto-completion).
```
typer tioj.py
```

## Current Development Environment

- Python 3.8.10
    - typer 0.6.1
    - rich 12.5.1
    - requests 2.25.1
    - bs4 4.10.0 
    - json 2.0.9
    - html_form_to_dict 2022.8.1
