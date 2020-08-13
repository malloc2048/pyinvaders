import logging
import unittest
import numpy as np
from common.constants import DataSrcDst
from hardware.i8080.registers import Registers


class FlagsTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.registers = Registers()

    def test_set_get_registers(self):
        self.registers.write_register(DataSrcDst.B, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.B))

        self.registers.write_register(DataSrcDst.C, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.C))

        self.registers.write_register(DataSrcDst.D, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.D))

        self.registers.write_register(DataSrcDst.E, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.E))

        self.registers.write_register(DataSrcDst.H, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.H))

        self.registers.write_register(DataSrcDst.L, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.L))

        self.registers.write_register(DataSrcDst.M, np.uint16(0x55aa))
        self.assertEqual(0, self.registers.read_register(DataSrcDst.M))

        self.registers.write_register(DataSrcDst.A, np.uint16(0x55aa))
        self.assertEqual(0xaa, self.registers.read_register(DataSrcDst.A))

        self.registers.write_register(DataSrcDst.BC, np.uint16(0x55aa))
        self.assertEqual(0x55aa, self.registers.read_register(DataSrcDst.BC))

        self.registers.write_register(DataSrcDst.DE, np.uint16(0x55aa))
        self.assertEqual(0x55aa, self.registers.read_register(DataSrcDst.DE))

        self.registers.write_register(DataSrcDst.HL, np.uint16(0x55aa))
        self.assertEqual(0x55aa, self.registers.read_register(DataSrcDst.HL))

        self.registers.write_register(DataSrcDst.SP, np.uint16(0x55aa))
        self.assertEqual(0x55aa, self.registers.read_register(DataSrcDst.SP))
