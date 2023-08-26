import sys
import matplotlib.pyplot as plt

sys.path.append("../../")

from mecode import G

g = G()
g.set_pressure(3,30)
g.feed(20)
g.toggle_pressure(3) # ON
x_pts, y_pts = g.square_spiral(n_turns=5, spacing=1, color=(1,0,0,0.6))
g.toggle_pressure(3) # OFF

g.abs_move(x=20, y=0)

g.toggle_pressure(3) # ON
x_pts, y_pts = g.square_spiral(n_turns=5, spacing=1, origin=(20,0),color=(0,0,1,0.6))
g.toggle_pressure(3) # OFF

g.teardown()

g.view(backend='matplotlib')
