ground
======

[![](https://github.com/lycantropos/ground/workflows/CI/badge.svg)](https://github.com/lycantropos/ground/actions/workflows/ci.yml "Github Actions")
[![](https://readthedocs.org/projects/ground/badge/?version=latest)](https://ground.readthedocs.io/en/latest "Documentation")
[![](https://codecov.io/gh/lycantropos/ground/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/ground "Codecov")
[![](https://img.shields.io/github/license/lycantropos/ground.svg)](https://github.com/lycantropos/ground/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/ground.svg)](https://badge.fury.io/py/ground "PyPI")

Summary
-------

`ground` is a pure Python library that provides protocols
for planar computational geometry models & operations
to unify interaction between different libraries
and allow customization.

---

In what follows `python` is an alias for `python3.6` or `pypy3.6`
or any later version (`python3.7`, `pypy3.7` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository
```bash
python -m pip install --upgrade ground
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/ground.git
cd ground
```

Install dependencies
```bash
python -m pip install -r requirements.txt
```

Install
```bash
python setup.py install
```

Usage
-----
```python
>>> from ground.base import get_context
>>> context = get_context()
>>> Multipoint = context.multipoint_cls
>>> Point = context.point_cls
>>> Segment = context.segment_cls
>>> origin = Point(0, 0)
>>> x_unit = Point(1, 0)
>>> y_unit = Point(0, 1)
>>> from ground.base import Kind
>>> context.angle_kind(origin, x_unit, y_unit) is Kind.RIGHT
True
>>> from ground.base import Orientation
>>> (context.angle_orientation(origin, x_unit, y_unit)
...  is Orientation.COUNTERCLOCKWISE)
True
>>> context.cross_product(origin, x_unit, origin, y_unit) == 1
True
>>> context.dot_product(origin, x_unit, origin, y_unit) == 0
True
>>> context.multipoint_centroid(Multipoint([origin])) == origin
True
>>> (context.points_convex_hull([origin, x_unit, y_unit])
...  == [origin, x_unit, y_unit])
True
>>> context.segment_contains_point(Segment(origin, x_unit), y_unit)
False
>>> context.segment_contains_point(Segment(origin, x_unit), origin)
True
>>> context.segments_intersection(Segment(origin, x_unit),
...                               Segment(origin, y_unit)) == origin
True
>>> from ground.base import Relation
>>> context.segments_relation(Segment(origin, x_unit),
...                           Segment(origin, y_unit)) is Relation.TOUCH
True

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies
```bash
python -m pip install -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script:
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script:
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
