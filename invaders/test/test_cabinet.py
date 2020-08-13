import logging
import unittest
import numpy as np
from common.config import Config
from hardware.cabinet import Cabinet


class CabinetTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.cfg = Config()
        self.cfg.items['rom_filename'] = '../../roms/invaders'
        self.cfg.items['instruction_set'] = '../../roms/instruction_set.csv'
        self.cabinet = Cabinet(self.cfg)

    def test_construction(self):
        self.assertEqual(self.cfg, self.cabinet.cfg)
        self.assertNotEqual(0, len(self.cabinet.cpu.instructions))
        self.assertEqual(np.ubyte(8), self.cabinet.next_interrupt)
        self.assertEqual(np.ubyte(0), self.cabinet.shift0)
        self.assertEqual(np.ubyte(0), self.cabinet.shift1)
        self.assertEqual(np.ubyte(0x08), self.cabinet.port1)
        self.assertEqual(np.ubyte(0x03), self.cabinet.port2)
        self.assertEqual(np.ubyte(0), self.cabinet.shift_offset)

    def test_interrupt(self):
        self.cabinet.cpu.registers.program_counter = 0x05af
        self.cabinet.cpu.registers.stack_pointer = 0x2300
        self.cabinet.cpu.flags.interrupt_enabled = True
        cpu_cycles = self.cabinet.cpu.cycles + 11

        self.cabinet.interrupt(np.ushort(0x03))

        self.assertEqual(cpu_cycles, self.cabinet.cpu.cycles)
        self.assertFalse(self.cabinet.cpu.flags.interrupt_enabled)
        self.assertEqual(0x22fe, self.cabinet.cpu.registers.stack_pointer)
        self.assertEqual(0x0003, self.cabinet.cpu.registers.program_counter)
        self.assertEqual(0x05af, self.cabinet.memory.read_word(self.cabinet.cpu.registers.stack_pointer))

    def test_helpers(self):
        self.cabinet.set_accumulator(np.ubyte(0xaa))
        self.assertEqual(0xaa, self.cabinet.get_accumulator())

        self.cabinet.set_cycle_count(np.ushort(0x1234))
        self.assertEqual(0x1234, self.cabinet.get_cycle_count())

        self.cabinet.increment_program_counter(np.ushort(0x1234))
        self.assertEqual(0x1234, self.cabinet.get_program_counter())
