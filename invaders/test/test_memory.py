import logging
import unittest
import numpy as np
from invaders.hardware.memory import Memory


class MemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.memory = Memory()

    def test_byte_operations(self):
        self.memory.write_byte(np.ushort(0x0000), np.ubyte(0xaa))
        self.assertEqual(0x00, self.memory.read_byte(np.ushort(0x0000)))

        self.memory.write_byte(np.ushort(0x2000), np.ubyte(0xaa))
        self.assertEqual(0xaa, self.memory.read_byte(np.ushort(0x2000)))

    def test_word_operations(self):
        self.memory.write_word(np.ushort(0x2000), np.ushort(0xaa55))
        self.assertEqual(0xaa55, self.memory.read_word(np.ushort(0x2000)))

    def test_load_rom(self):
        self.memory.load_rom('not_a_file')
        for adr in range(0x2000):
            self.assertEqual(0x00, self.memory.read_byte(np.ushort(adr)))

        self.memory.load_rom('../../roms/invaders')
        self.assertNotEqual(0x00, self.memory.read_byte(np.ushort(0x0003)))
