import numpy as np


class Instruction(object):
    def __init__(self, size=0, cycles=0, opcode=0, mnemonic='', operation=None):
        self.size = np.ubyte(size)
        self.operation = operation
        self.cycles = np.uint(cycles)
        self.mnemonic = str(mnemonic)
        self.opcode = np.ubyte(opcode)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
