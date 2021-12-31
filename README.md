# Twitter tools

[![PyPI](https://img.shields.io/pypi/v/twitter-tools?style=flat-square)](https://pypi.python.org/pypi/twitter-tools/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitter-tools?style=flat-square)](https://pypi.python.org/pypi/twitter-tools/)
[![PyPI - License](https://img.shields.io/pypi/l/twitter-tools?style=flat-square)](https://pypi.python.org/pypi/twitter-tools/)


---

**Documentation**: [https://namuan.github.io/twitter-tools](https://namuan.github.io/twitter-tools)

**Source Code**: [https://github.com/namuan/twitter-tools](https://github.com/namuan/twitter-tools)

**PyPI**: [https://pypi.org/project/twitter-tools/](https://pypi.org/project/twitter-tools/)

---

Collection of twitter utilities.

## Installation

```sh
pip install twitter-tools
```

## Example Usage

```shell

```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Validating build

```sh
make build
```

### Release process

A release is automatically published when a new version is bumped using `make bump`.
See `.github/workflows/build.yml` for more details.
Once the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.
