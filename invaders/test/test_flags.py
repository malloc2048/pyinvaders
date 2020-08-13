import logging
import unittest
import numpy as np
from hardware.i8080.flags import Flags


class FlagsTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.flags = Flags()

    def test_calculate_parity(self):
        self.flags.calculate_parity(np.ubyte(0))
        self.assertTrue(self.flags.parity)

        self.flags.calculate_parity(np.ubyte(1))
        self.assertFalse(self.flags.parity)

        self.flags.calculate_parity(np.ubyte(3))
        self.assertTrue(self.flags.parity)