```python
from mecode import G

g = G()
g.move(10, 10)  # move 10mm in x and 10mm in y
g.arc(x=10, y=5, radius=20, direction='CCW')  # counterclockwise arc with a radius of 20
g.meander(5, 10, spacing=1)  # trace a rectangle meander with 1mm spacing between passes
g.abs_move(x=1, y=1)  # move the tool head to position (1, 1)
g.home()  # move the tool head to the origin (0, 0)
g.teardown()

fig, ax = plt.subplots()

# pass axes handle to [`view`][mecode.main.G.view] to allow for furhter plot manipulations
ax = g.view('2d', ax=ax)

plt.show()
```
