import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("../../")

from mecode import G
from mecode_viewer import plot3d, plot2d, animation

g = G()
g.feed(20)

n_layers = 30
p_list = np.linspace(0, 10, n_layers)
dz = 1


'''
    - case where starting from origin w/ printing={} works
    - case where move before setting any pressure doesnt work
        printing = {}
'''
g.move(x=10)

print(g.history[-1])

for j in range(n_layers):
    print('pressure', p_list[j], p_list.max() - p_list[j])
    g.set_pressure(3, p_list.max())
    g.set_pressure(5, p_list[j])
    if j==0: 
        g.toggle_pressure(3)
        g.toggle_pressure(5)
    print(g.history[-1]['PRINTING'])
    ''''
        TODO: CURRENTLY REQUIRE A MOVE TO UPDATE CURRENT STATE.
            ISSUE IS DUE TO RELYING ON `self.extruding` since it will be overwritten by following `set_pressure`

        TODO:
            COLOR MIXING CODE ISN' WORKING IN MECODE_VIEWER EITHER
    '''
    
    print(g.history[-1]['PRINTING'])
    # if j == 0:
    #     print('turn on pressure')
    #     g.toggle_pressure(3)
    #     g.toggle_pressure(5)
    '''start box'''
    g.move(x=10)
    g.move(y=10)
    g.move(x=-10)
    g.move(y=-10)
    '''end box'''
    g.move(z=dz)
print('turning off pressures')
g.toggle_pressure(3)
print(g.history[-1]['PRINTING'])
g.toggle_pressure(5)
print(g.history[-1]['PRINTING'])
g.move(x=-10)

# plot3d(g.history)
plot3d(g.history, colors=('red', 'blue'), num_colors=3)
# plot2d(g.history, colors=('red', 'blue'))
animation(g.history, colors=('red', 'blue'), num_colors=3)
# animation(g.history)
