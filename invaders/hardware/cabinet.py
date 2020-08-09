import numpy as np
from invaders.common.config import Config
from invaders.hardware.memory import Memory
from invaders.hardware.i8080.cpu import CPU


class Cabinet(object):
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.memory = Memory()
        self.cpu = CPU(self.memory, self.cfg)

        self.nextInterrupt = np.ubyte(0x08)
        self.screenBuffer = np.zeros((256, 224, 4))

        self.shift0 = np.ubyte(0)
        self.shift1 = np.ubyte(0)
        self.port1 = np.ubyte(0x08)
        self.port2 = np.ubyte(0x03)
        self.shiftOffset = np.ubyte(0)

    def get_program_counter(self) -> np.ushort:
        return self.cpu.registers.program_counter

    def get_cycle_count(self) -> np.uint:
        return self.cpu.cycles

    def interrupt(self, address: np.ushort):
        pass

    def set_cycle_count(self, count: np.ushort):
        pass

    def get_accumulator(self) -> np.ubyte:
        return np.ubyte(0)

    def set_accumulator(self, value: np.ubyte):
        pass

    def increment_program_counter(self, increment: np.ubyte):
        pass
