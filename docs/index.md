Mecode
======
  `
[![Unit Tests](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml/badge.svg)](https://github.com/rtellez700/mecode/actions/workflows/python-package.yml)

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

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mecode`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Installation](intall.md)

-   :fontawesome-brands-markdown:{ .lg .middle } __Matrix Transformation__

    ---

    Focus on your content and generate a responsive and searchable static site

    [:octicons-arrow-right-24: Transforms](tutorials/matrix-transformations.md)

-   :material-format-font:{ .lg .middle } __Multimaterial Support__

    ---

    Change the colors, fonts, language, icons, logo and more with a few lines

    [:octicons-arrow-right-24: Multimaterial](tutorials/multimaterial-printing.md)

-   :material-scale-balance:{ .lg .middle } __Visualization__

    ---

    Material for MkDocs is licensed under MIT and available on [GitHub]

    [:octicons-arrow-right-24: Visualizations](tutorials/visualization.md)

-    :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    Material for MkDocs is licensed under MIT and available on [GitHub]

    [:octicons-arrow-right-24: License](#)

</div>


<!-- ## TODO

- [ ] build out multi-nozzle support
    - [ ] include multi-nozzle support in view method.
- [ ] add ability to read current status of aerotech
  - [ ] turn off omnicure after aborted runs
- [ ] add support for identifying part bounds and specifying safe post print "parking" -->


## Credits

This software was developed by the [Lewis Lab][2] at Harvard University. It is based on Jack Minardi's[^1] codebase (https://github.com/jminardi/mecode) which is no longer maintained.

[^1]: <jack@minardi.org>
[2]: http://lewisgroup.seas.harvard.edu/