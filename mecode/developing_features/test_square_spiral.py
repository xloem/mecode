import sys, os
import matplotlib.pyplot as plt

sys.path.append("../../")

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from mecode import G
except:
    sys.path.append(os.path.abspath(os.path.join(HERE, '..', '..')))
    from mecode import G

g = G()
g.set_pressure(3,30)
g.feed(20)
# print(g.history[-1]['PRINTING'])
print(g.extrusion_state)
g.toggle_pressure(3) # ON
# print(g.history[-1]['PRINTING'])
print(g.extrusion_state)
g.square_spiral(n_turns=5, spacing=1, color=(1,0,0,0.6))
g.toggle_pressure(3) # OFF

# print(g.history[-1]['PRINTING'])
print(g.extrusion_state)
g.abs_move(x=20, y=0)
# print(g.history[-1]['PRINTING'])
print(g.extrusion_state)

g.toggle_pressure(3) # ON
# print(g.history[-1]['PRINTING'])
print(g.extrusion_state)
g.square_spiral(n_turns=5, spacing=1, color=(0,0,1,0.6))
g.toggle_pressure(3) # OFF

g.teardown()

g.view(backend='matplotlib')

g.export_points('test_square_spiral.csv')