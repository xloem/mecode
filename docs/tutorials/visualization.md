By passing an `axes` handle to [`view()`](/mecode/api-reference/mecode/#mecode.main.G.view) you can take advantage of all plotting features from [matplotlib](https://matplotlib.org).

## Example

```python
from mecode import G
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

g = G()

g.feed(1)

g.toggle_pressure(1)
g.serpentine(25, 5, 1, color=(1,0,0))
g.toggle_pressure(1)

g.teardown()

fig, ax = plt.subplots()
ax = g.view('2d', ax=ax)
ax.set_xlim(-5, 30)
ax.set_ylim(-2, 5)
ax.add_patch(Rectangle(
    (0,0), 25, (5-1)*1, lw=5, ec='dodgerblue', fc='none',  alpha=0.3)
    )
plt.show()
```


??? example "Generated Gcode"

    ```
    Running mecode v0.2.38
    G1 F1
    Call togglePress P1
    G1 X25.000000
    G1 Y1.000000
    G1 X-25.000000
    G1 Y1.000000
    G1 X25.000000
    G1 Y1.000000
    G1 X-25.000000
    G1 Y1.000000
    G1 X25.000000
    Call togglePress P1

    Approximate print time: 
            177.637 seconds 
            3.0 min 
            0.0 hrs
    ```

### Result: example using matplotlib patches.Rectangle 
![](/mecode/assets/images/visualization_example.png)