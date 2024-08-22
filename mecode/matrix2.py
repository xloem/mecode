import copy
import numpy as np
from mecode import G

class GMatrix(G):
    """This class passes points through a 2D transformation matrix before
    fowarding them to the G class.  A 2D transformation matrix was
    choosen over a 3D transformation matrix because GCode's ARC
    command cannot be arbitrary rotated in a 3 dimensions.

    This lets you write code like:

    def box(g, height, width):
        g.move(0, width)
        g.move(height, 0)
        g.move(0, -width)
        g.move(-height, 0)

    def boxes(g, height, width):
        g.push_matrix()
        box(g, height, width)
        g.rotate(math.pi/8)
        box(g, height, width)
        g.pop_matrix()

    To get two boxes at a 45 degree angle from each other.

    The 2D transformation matrices are arranged in a stack,
    similar to OpenGL.

    numpy is required.

    """
    def __init__(self, *args, **kwargs):
        super(GMatrix, self).__init__(*args, **kwargs)
        # self._matrix_setup()
        self.stack = [np.identity(3)]
        # self.position_savepoints = []

    def push_matrix(self):
        # Push a copy of the current matrix onto the stack
        self.stack.append(self.stack[-1].copy())

    def pop_matrix(self):
        # Pop the top matrix off the stack
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            raise IndexError("Cannot pop from an empty matrix stack")
        
    def apply_transform(self, transform):
        # Apply a transformation matrix to the current matrix
        self.stack[-1] = self.stack[-1] @ transform

    def get_current_matrix(self):
        # Get the current matrix (top of the stack)
        return self.stack[-1]
    
    def translate(self, x, y):
        # Create a translation matrix and apply it
        translation_matrix = np.array([
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1]
        ])
        self.apply_transform(translation_matrix)

    def rotate(self, angle):
        # Create a rotation matrix for the angle
        c = np.cos(angle)
        s = np.sin(angle)
        rotation_matrix = np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
        self.apply_transform(rotation_matrix)

    def scale(self, sx, sy):
        # Create a scaling matrix and apply it
        scaling_matrix = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])
        self.apply_transform(scaling_matrix)

    def abs_move(self, x=None, y=None, z=None, **kwargs):
        if x is None: x = self.current_position['x']
        if y is None: y = self.current_position['y']
        if z is None: z = self.current_position['z']

        # abs_move ends up invoking move, which means that
        # we don't need to do a matrix transform here.
        super(GMatrix, self).abs_move(x,y,z, **kwargs)

    def move(self, x=None, y=None, z=None, **kwargs):
        # (x,y,z) = self._matrix_transform(x,y,z)
        current_matrix = self.get_current_matrix()

        if x is None: x = 0
        if y is None: y = 0
        if z is None: z = 0

        x, y, z = current_matrix @ np.array([x, y, z])

        super(GMatrix, self).move(x, y, z, **kwargs)
    
    # @property
    # def current_position(self):
    #     # x = self._current_position['x']
    #     # y = self._current_position['y']
    #     # z = self._current_position['z']

    #     # Ensure x and y are not None; default to 0.0
    #     # if x is None: x = 0.0
    #     # if y is None: y = 0.0

    #     # Get the latest matrix from the stack
    #     current_matrix = self.get_current_matrix()
    #     inverse_matrix = np.linalg.inv(current_matrix)

    #     # TODO: INVERSE OR CURRENT_MATRIX ???
    #     # x, y, z = current_matrix @ np.array([x, y, z])
    #     x_p, y_p, _ = current_matrix @ np.array([
    #         self._current_position['x'],
    #         self._current_position['y'],
    #         self._current_position['z']
    #     ])

    #     transformed_position = {**self._current_position}
    #     print('>>current position ', self._current_position)
    #     transformed_position.update({'x': x_p, 'y': y_p, 'z': self._current_position['z']})
    #     # return {'x': x, 'y': y, 'z': z_p}
    #     return transformed_position