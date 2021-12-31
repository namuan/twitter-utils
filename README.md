# Twitter tools

[![PyPI](https://img.shields.io/pypi/v/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)
[![PyPI - License](https://img.shields.io/pypi/l/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)


---

**Documentation**: [https://namuan.github.io/twitter-utils](https://namuan.github.io/twitter-utils)

**Source Code**: [https://github.com/namuan/twitter-utils](https://github.com/namuan/twitter-utils)

**PyPI**: [https://pypi.org/project/twitter-utils/](https://pypi.org/project/twitter-utils/)

---

Collection of twitter utilities.

## Installation

```sh
pip install twitter-utils
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
