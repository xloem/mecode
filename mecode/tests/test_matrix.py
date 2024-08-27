#! /usr/bin/env python

from os.path import abspath, dirname, join
import unittest
import sys
import math
import numpy as np

HERE = dirname(abspath(__file__))

try:
    from mecode import GMatrix
except:
    sys.path.append(abspath(join(HERE, "..", "..")))
    from mecode import GMatrix

from test_main import TestGFixture


class TestGMatrix(TestGFixture):
    def getGClass(self):
        return GMatrix

    def test_matrix_push_pop(self):
        self.g.feed(10)
        # See if we can rotate rectangle drawing by 90 degrees.
        self.g.push_matrix()
        self.g.rotate(math.pi / 2)
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

        # This makes sure that the pop matrix worked.
        self.g.rect(10, 5)
        self.expect_cmd("""
        G1 X0.000000 Y5.000000;
        G1 X10.000000 Y0.000000;
        G1 X0.000000 Y-5.000000;
        G1 X-10.000000 Y0.000000;
        """)
        self.assert_output()
        self.assert_position({"x": 0, "y": 0, "z": 0})

    def test_multiple_matrix_operations(self):
        self.g.feed(10)
        # See if we can rotate our rectangel drawing by 90 degrees, but
        # get to 90 degress by rotating twice.
        self.g.push_matrix()
        self.g.rotate(math.pi / 4)
        self.g.rotate(math.pi / 4)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G1 F10
        G1 X-5.000000 Y0.000000;
        G1 X0.000000 Y10.000000;
        G1 X5.000000 Y-0.000000;
        G1 X-0.000000 Y-10.000000;
        """)
        self.g.pop_matrix()
        self.assert_output()
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})

    def test_matrix_scale(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.scale(2, 2)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G1 F10
        G1 X0.000000 Y10.000000;
        G1 X20.000000 Y0.000000;
        G1 X0.000000 Y-10.000000;
        G1 X-20.000000 Y0.000000;
        """)
        self.g.pop_matrix()
        self.assert_output()

    def test_abs_move_and_rotate(self):
        self.g.feed(10)
        self.g.abs_move(x=5.0)
        self.assert_almost_position({"x": 5.0, "y": 0, "z": 0})

        self.g.rotate(math.pi)
        self.g.abs_move(x=5.0)
        self.assert_almost_position({"x": -5.0, "y": 0, "z": 0})

    def test_abs_zmove_with_rotate(self):
        self.g.feed(10)
        self.g.rotate(math.pi / 2.0)
        self.g.abs_move(x=1)
        self.assert_almost_position({"x": 0, "y": 1, "z": 0})

        self.g.pop_matrix()
        self.g.abs_move(z=2)
        self.assert_almost_position({'x': 0, 'y': 1, 'z': 2})


        self.expect_cmd("""
        G1 F10
        G90
        G1 X0.000000 Y1.000000 Z0.000000;
        G91
        G90
        G1 X0.000000 Y1.000000 Z2.000000;
        G91
        """)
        self.assert_output()

    def test_scale_and_abs_move(self):
        self.g.feed(10)
        self.g.scale(2.0, 2.0)
        self.g.abs_move(x=1)
        self.assert_almost_position({"x": 2, "y": 0, "z": 0})


    @unittest.skip("Skipping `test_arc` until arc function is fixed")
    def test_arc(self):
        self.g.feed(10)
        self.g.rotate(math.pi / 2)
        self.g.arc(x=10, y=0, linearize=False)
        self.expect_cmd("""
        G1 F10
        G17
        G2 X0.000000 Y10.000000 R5.000000
        """)
        self.assert_output()
        self.assert_almost_position({"x": 10, "y": 0, "z": 0})

    def test_current_position(self):
        self.g.feed(10)
        self.g.push_matrix()
        self.g.move(5, 0)
        self.assert_almost_position({"x": 5, "y": 0, "z": 0})

        self.g.move(-5, 0)
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})

        self.g.rotate(np.pi / 4)
        self.g.move(1, 0)

        self.assertAlmostEqual(math.cos(math.pi / 4), self.g._current_position["x"])
        self.assertAlmostEqual(math.cos(math.pi / 4), self.g._current_position["y"])

        self.g.move(-1, 0)
        self.g.pop_matrix()
        self.assert_almost_position({"x": 0, "y": 0, "z": 0})

        self.g.move(0, 0, -1)
        self.assert_almost_position({"x": 0, "y": 0, "z": -1})

    @unittest.skip("Skipping `test_matrix` - will likely deprecate this")
    def test_matrix_math(self):
        self.g.feed(10)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 2.0)
        self.g.rotate(math.pi / 3)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 2.0)
        self.g.scale(2.0, 2.0)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 4.0)
        self.g.scale(0.25, 0.25)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 1.0)

    def test_move(self):
        self.g.feed(1)
        self.g.move(10, 10)
        self.assert_position({"x": 10.0, "y": 10.0, "z": 0})

        self.g.move(10, 10, A=50)
        self.assert_position({"x": 20.0, "y": 20.0, "A": 50, "z": 0})

        self.g.move(10, 10, 10)
        self.assert_position({"x": 30.0, "y": 30.0, "A": 50, "z": 10})

        self.expect_cmd("""
        G1 F1
        G1 X10.000000 Y10.000000;
        G1 X10.000000 Y10.000000 A50.000000;
        G1 X10.000000 Y10.000000 Z10.000000;
        """)
        self.assert_output()

        self.g.abs_move(20, 20, 0)
        self.expect_cmd("""
        G90
        G1 X20.000000 Y20.000000 Z0.000000;
        G91
        """)
        self.assert_output()


if __name__ == "__main__":
    unittest.main()
