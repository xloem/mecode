import sys

sys.path.append("../../")

from mecode import G

g = G()
g.set_pressure(3, 30)
g.feed(10)

points = [[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0], [0, 0, 0]]

g.abs_move(z=+1)
g.toggle_pressure(3)
for x, y, z in points:
    # print(x,y,z)
    g.abs_move(x, y, z)

# g.view(backend='vpython',nozzle_cam=True)
# [0.0,0.0,-0.5,100,1,100]
# [x, y, z, length, height, width]
g.view(backend="vpython", nozzle_cam=True, substrate_dims=[0, 0, 0, 50, 50, 50])
