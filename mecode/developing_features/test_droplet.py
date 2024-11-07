import sys
import os

sys.path.append("../../")

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from mecode import G
except:
    sys.path.append(os.path.abspath(os.path.join(HERE, "..", "..")))
    from mecode import G

g = G()
g.feed(10)

for j in range(10):
    g.toggle_pressure(5)  # ON
    g.move(x=+j / 10, color=(1, 0, 0))
    g.toggle_pressure(5)  # OFF
    g.move(x=2)

g.teardown()

g.view("3d", shape="droplet", radius=0.5)
# plot3d(g.history, shape='droplet', radius=0.5)
