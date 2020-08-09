import numpy as np
from invaders.common.config import Config
from invaders.hardware.memory import Memory
from invaders.hardware.i8080.flags import Flags
from invaders.hardware.i8080.registers import Registers


class CPU(object):
    def __init__(self, memory: Memory, cfg: Config):
        self.cfg = cfg
        self.memory = memory

        self.flags = Flags()
        self.cycles = np.uint(0)
        self.registers = Registers()

    def step(self):
        pass

    def load_instruction_set(self):
        pass

    def make_instruction(self):
        pass

    def next_byte(self) -> np.ubyte:
        return np.ubyte(0)
