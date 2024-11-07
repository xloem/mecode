import numpy as np
from mecode import G
import warnings


class GMatrix3D(G):
    """This class passes points through a 3D transformation matrix before
    forwarding them to the G class, allowing transformations in all three
    dimensions.

    The 3D transformation matrices are arranged in a stack, similar to OpenGL.

    numpy is required.
    """

    def __init__(self, *args, **kwargs):
        super(GMatrix3D, self).__init__(*args, **kwargs)
        self.stack = [np.identity(4)]  # Start with a 4x4 identity matrix

    def push_matrix(self):
        # Push a copy of the current matrix onto the stack
        self.stack.append(self.stack[-1].copy())

    def pop_matrix(self):
        # Pop the top matrix off the stack
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            self.stack = [np.identity(4)]
            warnings.warn(
                "Cannot pop all items from stack. Resetting to default identity matrix."
            )

    def apply_transform(self, transform):
        # Apply a transformation matrix to the current matrix
        transformed_matrix = self.stack[-1] @ transform

        # Round values smaller than machine epsilon to zero
        epsilon = np.finfo(transformed_matrix.dtype).eps
        self.stack[-1] = np.where(
            np.abs(transformed_matrix) < epsilon, 0, transformed_matrix
        )

    def get_current_matrix(self):
        # Get the current matrix (top of the stack)
        return self.stack[-1]

    def translate(self, x=0, y=0, z=0):
        # Create a 3D translation matrix and apply it
        translation_matrix = np.array(
            [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        )
        self.apply_transform(translation_matrix)

    def rotate_x(self, angle):
        # Create a rotation matrix around the X-axis
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array(
            [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]
        )
        self.apply_transform(rotation_matrix)

    def rotate_y(self, angle):
        # Create a rotation matrix around the Y-axis
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array(
            [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]
        )
        self.apply_transform(rotation_matrix)

    def rotate_z(self, angle):
        # Create a rotation matrix around the Z-axis
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array(
            [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        )
        self.apply_transform(rotation_matrix)

    def scale(self, sx, sy=None, sz=None):
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx
        # Create a scaling matrix and apply it
        scaling_matrix = np.array(
            [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        )
        self.apply_transform(scaling_matrix)

    def abs_move(self, x=None, y=None, z=None, **kwargs):
        if x is None:
            x = self.current_position["x"]
        if y is None:
            y = self.current_position["y"]
        if z is None:
            z = self.current_position["z"]
        super(GMatrix3D, self).abs_move(x, y, z, **kwargs)

    def move(self, x=None, y=None, z=None, **kwargs):
        x_p, y_p, z_p = self._transform_point(x, y, z)
        super(GMatrix3D, self).move(x_p, y_p, z_p, **kwargs)

    def _transform_point(self, x, y, z):
        current_matrix = self.get_current_matrix()

        if x is None:
            x = 0
        if y is None:
            y = 0
        if z is None:
            z = 0

        transformed_point = current_matrix @ np.array([x, y, z, 1])
        return transformed_point[:3]  # Return only x, y, z
