import sys
import matplotlib.pyplot as plt

sys.path.append("../../")

from mecode import G
from mecode_viewer import plot3d

g = G()
g.feed(20)

g.move(0,0,1, color=(0,1,0))
g.set_pressure(3,30)

g.toggle_pressure(3)
g.move(x=10, color=(1,0,0))
g.move(y=10, color=(1,0,0))
g.move(x=-10, color=(1,0,0))
g.move(y=-10, color=(1,0,0))
g.toggle_pressure(3)

g.move(z=10, color=(0,0,0))

g.set_pressure(5,13)
g.toggle_pressure(5)
g.move(x=10, color=(0,1,0))
g.move(y=10, color=(0,1,0))
g.move(x=-10, color=(0,1,0))
g.move(y=-10, color=(0,1,0))
g.toggle_pressure(5)
g.move(z=10, color=(0,0,0))


g.teardown()

# print(g.history)
# print(g.extruding_history)
g.view(backend='matplotlib')

# plot3d(g.history, colors=('red', 'blue'))
