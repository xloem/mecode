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
    sys.path.append(abspath(join(HERE, '..', '..')))
    from mecode import GMatrix

from test_main import TestGFixture

class TestGMatrix(TestGFixture):
    def getGClass(self):
        return GMatrix
    
    def test_move(self):
        self.g.feed(1)
        self.g.move(10, 10)
        self.assert_position({'x': 10.0, 'y': 10.0, 'z': 0})

        self.g.move(10, 10, A=50)
        self.assert_position({'x': 20.0, 'y': 20.0, 'A': 50, 'z': 0})

        self.g.move(10, 10, 10)
        self.assert_position({'x': 30.0, 'y': 30.0, 'A': 50, 'z': 10})

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

if __name__ == '__main__':
    unittest.main()