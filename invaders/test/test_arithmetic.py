import random
import logging
import unittest
import numpy as np
from hardware.memory import Memory
from hardware.i8080.flags import Flags
from common.constants import DataSrcDst
from hardware.i8080.registers import Registers
from hardware.i8080.operations.arithmetic import Arithmetic


class CabinetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.flags = Flags()
        self.memory = Memory()
        self.registers = Registers()
        self.arithmetic = Arithmetic(self.flags, self.memory, self.registers)

    def test_construction(self):
        self.assertEqual(self.flags, self.arithmetic.flags)
        self.assertEqual(self.memory, self.arithmetic.memory)
        self.assertEqual(self.registers, self.arithmetic.registers)

    def test_add(self):
        opcodes = [np.ubyte(0x80), np.ubyte(0x81), np.ubyte(0x82), np.ubyte(0x83), np.ubyte(0x84), np.ubyte(0x85)]
        for opcode in opcodes:
            src = opcode & 0x07
            self.registers.accumulator = 0
            value = np.ubyte(random.randint(0, 255))
            self.registers.write_register(src, value)

            self.arithmetic.execute(opcode)
            self.assertEqual((value) & 0xff, self.registers.accumulator)

        value = np.ubyte(random.randint(0, 255))
        self.registers.accumulator = value
        self.arithmetic.execute(np.ubyte(0x87))
        self.assertEqual((value * 2) & 0xff, self.registers.accumulator)

        self.registers.accumulator = 0
        value = np.ubyte(random.randint(0, 255))
        self.memory.write_byte(np.ushort(0x2000), value)
        self.registers.write_register(DataSrcDst.HL, np.ushort(0x2000))

        self.arithmetic.execute(np.ubyte(0x86))
        self.assertEqual((value) & 0xff, self.registers.accumulator)

    def test_add_with_carry(self):
        opcodes = [np.ubyte(0x88), np.ubyte(0x89), np.ubyte(0x8a), np.ubyte(0x8b), np.ubyte(0x8c), np.ubyte(0x8d)]
        for opcode in opcodes:
            src = opcode & 0x07
            self.flags.carry = True
            self.registers.accumulator = 0
            value = np.ubyte(random.randint(0, 255))
            self.registers.write_register(src, value)

            self.arithmetic.execute(opcode)
            self.assertEqual(value + 1, self.registers.accumulator)

            self.flags.carry = False
            self.arithmetic.execute(opcode)
            self.assertEqual(((value * 2) + 1) & 0xff, self.registers.accumulator)

        value = np.ubyte(random.randint(0, 255))
        self.flags.carry = True
        self.registers.accumulator = value
        self.arithmetic.execute(np.ubyte(0x8f))
        self.assertEqual((value * 2 + 1) & 0xff, self.registers.accumulator)

        self.flags.carry = False
        self.registers.accumulator = value
        self.arithmetic.execute(np.ubyte(0x8f))
        self.assertEqual((value * 2) & 0xff, self.registers.accumulator)

        self.flags.carry = True
        self.registers.accumulator = 0
        value = np.ubyte(random.randint(0, 255))
        self.memory.write_byte(np.ushort(0x2000), value)
        self.registers.write_register(DataSrcDst.HL, np.ushort(0x2000))

        self.arithmetic.execute(np.ubyte(0x8e))
        self.assertEqual((value + 1) & 0xff, self.registers.accumulator)
