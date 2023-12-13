Mecode
======
  `
[![Unit Tests](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml/badge.svg)](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml)

## Overview

Mecode is designed to simplify GCode generation. It is not a slicer, thus it
can not convert CAD models to 3D printer ready code. It simply provides a
convenient, human-readable layer just above GCode. If you often find
yourself manually writing your own GCode, then mecode is for you.

## Matrix Transforms

A wrapper class, `GMatrix` will run all move and arc commands through a 
2D transformation matrix before forwarding them to `G`.

To use, simply instantiate a `GMatrix` object instead of a `G` object:

```python
g = GMatrix()
g.push_matrix()      # save the current transformation matrix on the stack.
g.rotate(math.pi/2)  # rotate our transformation matrix by 90 degrees.
g.move(0, 1)         # same as moves (1,0) before the rotate.
g.pop_matrix()       # revert to the prior transformation matrix.
```

The transformation matrix is 2D instead of 3D to simplify arc support.

## Multimaterial Printing

When working with a machine that has more than one Z-Axis, it is
useful to use the `rename_axis()` function. Using this function your
code can always refer to the vertical axis as 'Z', but you can dynamically
rename it.

## Installation

The easiest method to install mecode is with pip:

```bash
pip install git+https://github.com/rtellez700/mecode.git
```

To install from source:

```bash
$ git clone https://github.com/rtellez700/mecode.git
$ cd mecode
$ pip install -r requirements.txt
$ python setup.py install
```


## TODO

- [ ] create github page
- [ ] build out multi-nozzle support
    - [ ] include multi-nozzle support in view method.
- [ ] add ability to read current status of aerotech
  - [ ] turn off omnicure after aborted runs
- [ ] add support for identifying part bounds and specifying safe post print "parking"


## Credits

This software was developed by the [Lewis Lab][2] at Harvard University. It is based on Jack Minardi's[^1] codebase (https://github.com/jminardi/mecode) which is no longer maintained.

[^1]: <jack@minardi.org>
[2]: http://lewisgroup.seas.harvard.edu/