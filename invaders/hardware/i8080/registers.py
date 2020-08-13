import numpy as np
from common.constants import DataSrcDst


class Registers(object):
    def __init__(self):
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0
        self.accumulator = 0

        self.stack_pointer = 0
        self.program_counter = 0

    def __str__(self):
        return str(self.__dict__)

    def read_register(self, reg):
        if DataSrcDst.B == DataSrcDst(reg):
            return self.b
        elif DataSrcDst.C == DataSrcDst(reg):
            return self.c
        elif DataSrcDst.D == DataSrcDst(reg):
            return self.d
        elif DataSrcDst.E == DataSrcDst(reg):
            return self.e
        elif DataSrcDst.H == DataSrcDst(reg):
            return self.h
        elif DataSrcDst.L == DataSrcDst(reg):
            return self.l
        elif DataSrcDst.A == DataSrcDst(reg):
            return self.accumulator
        elif DataSrcDst.BC == DataSrcDst(reg):
            bc = self.b << 0x08 | self.c
            return bc
        elif DataSrcDst.DE == DataSrcDst(reg):
            de = self.d << 0x08 | self.e
            return de
        elif DataSrcDst.HL == DataSrcDst(reg):
            hl = self.h << 0x08 | self.l
            return hl
        elif DataSrcDst.SP == DataSrcDst(reg):
            return self.stack_pointer
        else:
            return np.ushort(0)

    def write_register(self, reg, data):
        if DataSrcDst.B == DataSrcDst(reg):
            self.b = int(data & 0x00ff)
        elif DataSrcDst.C == DataSrcDst(reg):
            self.c = int(data & 0x00ff)
        elif DataSrcDst.D == DataSrcDst(reg):
            self.d = int(data & 0x00ff)
        elif DataSrcDst.E == DataSrcDst(reg):
            self.e = int(data & 0x00ff)
        elif DataSrcDst.H == DataSrcDst(reg):
            self.h = int(data & 0x00ff)
        elif DataSrcDst.L == DataSrcDst(reg):
            self.l = int(data & 0x00ff)
        elif DataSrcDst.A == DataSrcDst(reg):
            self.accumulator = int(data & 0x00ff)
        elif DataSrcDst.BC == DataSrcDst(reg):
            self.c = int(data & 0x00ff)
            self.b = int(data >> 0x08)
        elif DataSrcDst.DE == DataSrcDst(reg):
            self.e = int(data & 0x00ff)
            self.d = int(data >> 0x08)
        elif DataSrcDst.HL == DataSrcDst(reg):
            self.l = int(data & 0x00ff)
            self.h = int(data >> 0x08)
        elif DataSrcDst.SP == DataSrcDst(reg):
            self.stack_pointer = int(data)
