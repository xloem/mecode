Mecode
======

[![Unit Tests](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml/badge.svg)](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
![](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-maintained-yellow.svg)
[![](https://img.shields.io/github/license/rtellez700/mecode.svg)](https://github.com/rtellez700/mecode/blob/main/LICENSE.md)


### GCode for all

Mecode is designed to simplify GCode generation. It is not a slicer, thus it
can not convert CAD models to 3D printer ready code. It simply provides a
convenient, human-readable layer just above GCode. If you often find
yourself manually writing your own GCode, then mecode is for you.

Basic Use
---------
To use, simply instantiate the `G` object and use its methods to trace your
desired tool path.

```python
from mecode import G
g = G()
g.move(10, 10)  # move 10mm in x and 10mm in y
g.arc(x=10, y=5, radius=20, direction='CCW')  # counterclockwise arc with a radius of 20
g.meander(5, 10, spacing=1)  # trace a rectangle meander with 1mm spacing between passes
g.abs_move(x=1, y=1)  # move the tool head to position (1, 1)
g.home()  # move the tool head to the origin (0, 0)
```

By default `mecode` simply prints the generated GCode to stdout. If instead you
want to generate a file, you can pass a filename and turn off the printing when
instantiating the `G` object.

```python
g = G(outfile='path/to/file.gcode', print_lines=False)
```

*NOTE:* `g.teardown()` must be called after all commands are executed if you
are writing to a file. This can be accomplished automatically by using G as
a context manager like so:

```python
with G(outfile='file.gcode') as g:
    g.move(10)
```

When the `with` block is exited, `g.teardown()` will be automatically called.


Installation
------------

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

Documentation
-------------

Full documentation can be found at [https://rtellez700.github.io/mecode/](https://rtellez700.github.io/mecode/)


TODO
----

- [x] add formal documentation
- [x] create github page
- [x] build out multi-nozzle support
    - [x] include multi-nozzle support in view method
- [ ] add ability to read current status of aerotech
  - [ ] turn off omnicure after aborted runs
- [ ] add support for identifying part bounds and specifying safe post print "parking"
- [ ] add support for auto-generating aerotech specific functions only if needed.
  - [ ] add support for easily adding new serial devices: (1) pyserial-based, (2) aerotech, or (3) other??

Credits
-------
This software was developed by the [Lewis Lab][2] at Harvard University. It is based on Jack Minardi's (jack@minardi.org) codebase (https://github.com/jminardi/mecode) which is not maintained anymore.

[2]: http://lewisgroup.seas.harvard.edu/
