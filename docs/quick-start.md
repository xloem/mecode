## Basic Use

To use, simply instantiate the `G` object and use its methods to trace your
desired tool path.

```python
from mecode import G

g = G()

# move 10mm in x and 10mm in y
g.move(10, 10)  (1)

# counterclockwise arc with a radius of 20
g.arc(x=10, y=5, radius=20, direction='CCW')

# trace a rectangle meander with 1mm spacing between passes
g.meander(5, 10, spacing=1)

# move the tool head to position (1, 1)
g.abs_move(x=1, y=1)  

# move the tool head to the origin (0, 0)
g.home()
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

The resulting toolpath can be visualized in 3D using the [`matplotlib`](https://matplotlib.org/) or [`vpython`](https://vpython.org/)
package with the [`view()`](api-reference/mecode.md/#mecode.main.G.view) method:

```python
g = G()
g.meander(10, 10, 1)
g.view()
```

## Visualization
The graphics backend can be specified when calling the `view()` method and providing one of the following as the `backend` argument:

<div class="annotate" markdown>
- `2d` -- 2D visualization figure
- `3d` -- 3D visualization figure (1)
- `animated` -- animated rendering (2)
</div>
1.  `matplotlib` is also supported for backwards compatibility
2.  `vpython` is also supported for backwards compatibility


E.g.
```python
g.view('matplotlib')
```

Check out [tutorials/visualization](tutorials/visualization.md) for more advanced visualizations.