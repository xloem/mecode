For every printing move, `mecode` stores all relevant printing conditions, coordinates, etc inside a `history` list of `print_move` dictionaries. The schema of this dictionary is the following:

```python
{
    'REL_MODE': bool,
    'ACCEL' : float,
    'DECEL' : float,
    'PRINTING': {
        'extruder_id': {
            'printing': bool,
            'value': float
        }
    },
    'PRINT_SPEED': float,
    'COORDS': Tuple[float, float, float],
    'ORIGIN': Tuple[float, float, float],
    'CURRENT_POSITION': {'X': float, 'Y': float, 'Z': float},
    'COLOR': Tuple[float, float, float]
}
```

The first entry in the list is given as the origin and with default acceleration, deceleration, and origin

```python
history = [{
    'REL_MODE': True,
    'ACCEL' : 2500,
    'DECEL' : 2500,
    'PRINTING': {},
    'PRINT_SPEED': 0,
    'COORDS': (0,0,0),
    'ORIGIN': (0,0,0),
    'CURRENT_POSITION': {'X': 0, 'Y': 0, 'Z': 0},
    'COLOR': None
}]
```

Descriptions

| Variable | Description |
| -------- | ----------- |
| `REL_MODE` | True if the current `print_move` is in relative coordinates |
| `ACCEL` | Printer acceleration in mm/s^2 |
| `DECEL` | Printer deceleration in mm/s^2 |
| `PRINTING` | `dict` that contains current printing/extrusion state |
| `PRINTING[extruder_id]` | Once an extrusion source is turned on, `mecode` automatically adds a printing state to `PRINTING` that can be accessed via `PRINTING['extruder_id']` |
| `PRINTING[extruder_id]['printing]` | Once `extruder_id` is created, you can check if this source is currently extruding via `PRINTING[extruder_id][printing]` |
| `PRINTING[extruder_id]['printing]` | Once `extruder_id` is created, you can check what extrusion rate is (in instrument units, e.g., psi for Nordson pressuder adapter) via `PRINTING[extruder_id][value]` |
| `PRINTING_SPEED` | Printer speed in mm/s |
| `COORDS` | Current `print_move`'s, relative or absolute, coordinates in determined by `REL_MODE` |
| `ORIGIN` | Current definition of origin. A G92 command will overwrite this |
| `CURRENT_POSITION` | Hold current absolute coordinates of printer, with relative/absolute mode already taken into account |
| `COLOR` | Color of current `print_move`. Useful for specifying custom filament color--especially for multimaterial printing |

In `mecode`, the printing history, e.g., to use in a third-party package or own python, can be accessed via `g.history[...]`. Where `g.history[n]` specifies the `n`^th^ `print_move`.