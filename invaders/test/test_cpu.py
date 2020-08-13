import logging
import unittest
import numpy as np
from common.config import Config
from hardware.i8080.cpu import CPU
from hardware.memory import Memory


class MockOperation:
    def __init__(self):
        pass

    def execute(self, opcode: np.ubyte):
        pass


class MockInstruction(object):
    def __init__(self):
        self.cycles = 1
        self.operation = MockOperation()


class CPUTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.cfg = Config()
        self.cfg.items['rom_filename'] = '../../roms/invaders'
        self.cfg.items['instruction_set'] = '../../roms/instruction_set.csv'

        self.memory = Memory()
        self.cpu = CPU(self.memory, self.cfg)

    def test_construction(self):
        self.assertEqual(self.cfg, self.cpu.cfg)
        self.assertEqual(self.memory, self.cpu.memory)

    def test_step(self):
        for i in range(0, 10):
            self.memory.rom[i] = i
            self.cpu.instructions[i] = MockInstruction()

        self.cpu.step()
        self.assertEqual(1, self.cpu.cycles)
        self.assertEqual(1, self.cpu.registers.program_counter)
