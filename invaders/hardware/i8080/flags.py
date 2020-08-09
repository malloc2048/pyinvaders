import numpy as np


class Flags(object):
    def __init__(self):
        self.sign = False
        self.zero = False
        self.carry = False
        self.parity = False
        self.half_carry = False

        self.halted = False
        self.interrupt_enabled = False

    def calculate_parity(self, value: np.ubyte):
        bits_set = 0
        for i in range(0, 8):
            if value & (0x01 << i):
                bits_set += 1
        self.parity = (bits_set & 0x01) == 0
