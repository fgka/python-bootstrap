# Python Production Project Bootstrap

The goal here is to provide a somewhat production ready python project 
bootstrap. Simply put, clone it and have ready starting point for you python 
project.

## Development 

Below how to bootstrap your python environment so it is sandboxed.

### Development Environment Using Pyenv and Virtualenv

#### macOS requirements

You need `Xcode`:
```bash
xcode-select --install
```

#### Pyenv

For macOS follow [https://gist.github.com/eliangcs/43a51f5c95dd9b848ddc](https://gist.github.com/eliangcs/43a51f5c95dd9b848ddc).
You might also need [https://github.com/jiansoung/issues-list/issues/13#issuecomment-478575934](https://github.com/jiansoung/issues-list/issues/13#issuecomment-478575934).

Set python 3.7 as default:
```basn
pyenv install 3.7.3
```

Set pyenv defaults:
```bash
pyenv global 3.7.3
pyenv local 3.7.3
```

#### Virtualenv

Install Virtualenv and update `pip`:
```bash
pip3.7 install -U pip virtualenv
```

Create virtualenv:
```bash
cd <Your project root dir>

virtualenv -p python3.7 -q .venv
```

To activate your python virtualenv:
```bash
. .venv/bin/activate
```

Validate with:
```bash
python --version
python3 --version
```

### Install all dependencies

Install packages:
```bash
python setup.py develop
```

### Auto-formatting with black

In this project black was chosen for the auto-formatter.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

