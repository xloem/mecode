import math
import sys
from os.path import abspath, dirname, join

HERE = dirname(abspath(__file__))

try:
    from mecode import GMatrix
except:
    sys.path.append(abspath(join(HERE, '..', '..')))
    from mecode import GMatrix


g = GMatrix()

g.feed(1)

# g.toggle_pressure(1)
g.push_matrix()      # save the current transformation matrix on the stack.
g.rotate(math.pi/2)  # rotate our transformation matrix by 90 degrees.
# g.serpentine(25, 5, 1, color=(1,0,0))         # same as moves (1,0) before the rotate.
g.rect(10, 5)
g.pop_matrix()       # revert to the prior transformation matrix.

g.teardown()