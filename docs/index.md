Mecode
======
  `
[![Unit Tests](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml/badge.svg)](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml) ![](https://img.shields.io/badge/python-3.0+-blue.svg) ![t](https://img.shields.io/badge/status-maintained-yellow.svg) [![](https://img.shields.io/github/license/rtellez700/mecode.svg)](https://github.com/rtellez700/mecode/blob/main/LICENSE.md)

## Overview

Mecode is designed to simplify GCode generation. It is not a slicer, thus it
can not convert CAD models to 3D printer ready code. It simply provides a
convenient, human-readable layer just above GCode. If you often find
yourself manually writing your own GCode, then mecode is for you.

<!-- 
  - gcode generation
  - matrix transformation
  - multimaterial support
  - visualization tools
 -->

## Why [`mecode`](#)?
<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mecode`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Installation](install.md)

-   :material-format-rotate-90:{ .lg .middle } __Matrix Transformation__

    ---

    [`mecode`](#) is capable of transforming toolpaths (e.g., rotation matrices).

    [:octicons-arrow-right-24: Transforms](tutorials/matrix-transformations.md)

    
-   :material-multicast:{ .lg .middle } __Multimaterial Support__

    ---

    Multimaterial support enabled on multiaxis printers via [`rename_axis`](/api-reference/mecode/#mecode.main.G.rename_axis)

    [:octicons-arrow-right-24: Multimaterial example](tutorials/multimaterial-printing.md)

-   :material-chart-scatter-plot-hexbin:{ .lg .middle } __Visualization__

    ---

    Gcode toolpath visualization enabled by [matplotlib](https://matplotlib.org/) with color coding support for complex prints.

    [:octicons-arrow-right-24: Visualizations](tutorials/visualization.md)

-   :material-serial-port:{ .lg .middle } __Serial Communication__

    ---

    With the option `direct_write=True`, a serial connection to a Printer can be established via USB serial at a virtual COM port (e.g., RS-232).

    [:octicons-arrow-right-24: Direct connection](tutorials/serial-communication.md)

-    :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    [`mecode`](#) is licensed under MIT and available on [GitHub](https://github.com/rtellez700/mecode) or the [License tab](license.md)

    [:octicons-arrow-right-24: License](#)

</div>


<!-- ## TODO

- [x] build out multi-nozzle support
    - [x] include multi-nozzle support in view method.
- [ ] add ability to read current status of aerotech
  - [ ] turn off omnicure after aborted runs
- [ ] add support for identifying part bounds and specifying safe post print "parking" -->


## Credits

This software was developed by the [Lewis Lab][2] at Harvard University. It is based on Jack Minardi's[^1] codebase (https://github.com/jminardi/mecode) which is no longer maintained.

[^1]: <jack@minardi.org>
[2]: http://lewisgroup.seas.harvard.edu/