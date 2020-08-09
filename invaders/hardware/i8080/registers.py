import numpy as np
from invaders.common.constants import DataSrcDst


class Registers(object):
    def __init__(self):
        self.b = np.ubyte(0)
        self.c = np.ubyte(0)
        self.d = np.ubyte(0)
        self.e = np.ubyte(0)
        self.h = np.ubyte(0)
        self.l = np.ubyte(0)
        self.accumulator = np.ubyte(0)

        self.stack_pointer = np.ushort(0)
        self.program_counter = np.ushort(0)

    def read_register(self, reg: np.ubyte) -> np.ushort:
        if DataSrcDst.B == reg:
            return self.b
        elif DataSrcDst.C == reg:
            return self.c
        elif DataSrcDst.D == reg:
            return self.d
        elif DataSrcDst.E == reg:
            return self.e
        elif DataSrcDst.H == reg:
            return self.h
        elif DataSrcDst.L == reg:
            return self.l
        elif DataSrcDst.A == reg:
            return self.accumulator
        elif DataSrcDst.BC == reg:
            bc = self.b << 0x08 | self.c
            return bc
        elif DataSrcDst.DE == reg:
            de = self.d << 0x08 | self.e
            return de
        elif DataSrcDst.HL == reg:
            hl = self.h << 0x08 | self.l
            return hl
        elif DataSrcDst.SP == reg:
            return self.stack_pointer
        else:
            return np.ushort(0)

    def write_register(self, reg: np.ubyte, data: np.ushort):
        if DataSrcDst.B == reg:
            self.b = data & 0x00ff
        elif DataSrcDst.C == reg:
            self.c = data & 0x00ff
        elif DataSrcDst.D == reg:
            self.d = data & 0x00ff
        elif DataSrcDst.E == reg:
            self.e = data & 0x00ff
        elif DataSrcDst.H == reg:
            self.h = data & 0x00ff
        elif DataSrcDst.L == reg:
            self.l = data & 0x00ff
        elif DataSrcDst.A == reg:
            self.accumulator = data & 0x00ff
        elif DataSrcDst.BD == reg:
            self.c = data & 0x00ff
            self.b = data >> 0x08
        elif DataSrcDst.DE == reg:
            self.d = data & 0x00ff
            self.e = data >> 0x08
        elif DataSrcDst.HL == reg:
            self.l = data & 0x00ff
            self.h = data >> 0x08
        elif DataSrcDst.SP == reg:
            self.stack_pointer = data
