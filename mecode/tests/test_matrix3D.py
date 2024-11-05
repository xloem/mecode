#!/usr/bin/env python

from os.path import abspath, dirname, join
import unittest
import sys
import math
import numpy as np

HERE = dirname(abspath(__file__))

try:
    from mecode import GMatrix3D
except ImportError:
    sys.path.append(abspath(join(HERE, "..", "..")))
    from mecode import GMatrix3D

from test_main import TestGFixture


class TestGMatrix3D(TestGFixture):
    def getGClass(self):
        return GMatrix3D

    def test_3d_translate(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.translate(5, 5, 5)
        self.g.abs_move(x=0, y=0, z=0)
        self.assert_almost_position({"x": 5, "y": 5, "z": 5})
        self.g.pop_matrix()

    def test_3d_rotate_x(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.rotate_x(math.pi / 2)
        self.g.move(0, 1, 0)
        self.assert_almost_position({"x": 0, "y": 0, "z": 1})
        self.g.pop_matrix()

    def test_3d_rotate_y(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.rotate_y(math.pi / 2)
        self.g.move(1, 0, 0)
        self.assert_almost_position({"x": 0, "y": 0, "z": -1})
        self.g.pop_matrix()

    def test_3d_rotate_z(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.rotate_z(math.pi / 2)
        self.g.move(1, 0, 0)
        self.assert_almost_position({"x": 0, "y": 1, "z": 0})
        self.g.pop_matrix()

    def test_3d_scale(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.scale(2, 2, 2)
        self.g.abs_move(x=1, y=1, z=1)
        self.assert_almost_position({"x": 2, "y": 2, "z": 2})
        self.g.pop_matrix()

    def test_matrix_push_pop(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.rotate_z(math.pi / 2)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G1 F10
        G1 X-5.000000 Y0.000000;
        G1 X0.000000 Y10.000000;
        G1 X5.000000 Y0.000000;
        G1 X0.000000 Y-10.000000;
        """)
        self.g.pop_matrix()
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})
        self.g.rect(10, 5)
        self.expect_cmd("""
        G1 X0.000000 Y5.000000;
        G1 X10.000000 Y0.000000;
        G1 X0.000000 Y-5.000000;
        G1 X-10.000000 Y0.000000;
        """)
        self.assert_output()
        self.assert_position({"x": 0, "y": 0, "z": 0})

    def test_abs_move_with_3d_transformations(self):
        self.g.feed(10)
        self.g.translate(3, 3, 3)
        self.g.abs_move(x=1, y=1, z=1)
        self.assert_almost_position({"x": 4, "y": 4, "z": 4})

    def test_current_position(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.move(5, 0, 0)
        self.assert_almost_position({"x": 5, "y": 0, "z": 0})
        self.g.move(-5, 0, 0)
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})
        self.g.rotate_z(np.pi / 4)
        self.g.move(1, 0, 0)
        self.assertAlmostEqual(math.cos(math.pi / 4), self.g._current_position["x"])
        self.assertAlmostEqual(math.cos(math.pi / 4), self.g._current_position["y"])
        self.g.move(-1, 0, 0)
        self.g.pop_matrix()
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})
        self.g.move(0, 0, -1)
        self.assert_almost_position({"x": 0, "y": 0, "z": -1})

    def test_3d_move_and_scale(self):
        self.g.feed(10)
        self.g.scale(2.0, 2.0, 2.0)
        self.g.abs_move(x=1, y=1, z=1)
        self.assert_almost_position({"x": 2, "y": 2, "z": 2})

    @unittest.skip("Skipping `test_arc` until arc function is fixed")
    def test_arc(self):
        self.g.feed(10)
        self.g.rotate_z(math.pi / 2)
        self.g.arc(x=10, y=0, linearize=False)
        self.expect_cmd("""
        G1 F10
        G17
        G2 X0.000000 Y10.000000 R5.000000
        """)
        self.assert_output()
        self.assert_almost_position({"x": 10, "y": 0, "z": 0})


if __name__ == "__main__":
    unittest.main()
