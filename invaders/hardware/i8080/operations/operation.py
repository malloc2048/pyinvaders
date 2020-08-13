import numpy as np
from common.constants import DataSrcDst


class Operation(object):
    @staticmethod
    def next_byte(cpu) -> np.ubyte:
        value = cpu.memory.read_byte(cpu.registers.program_counter)
        cpu.registers.program_counter += 1
        return value

    @staticmethod
    def next_word(cpu) -> np.ushort:
        value = Operation.next_byte(cpu)
        value |= np.ushort(Operation.next_byte(cpu) << 8)
        return value

    @staticmethod
    def get_data(src: np.ubyte, cpu) -> np.ushort:
        if DataSrcDst(src) == DataSrcDst.M:
            return cpu.memory.read_byte(cpu.registers.read_register(DataSrcDst.HL))
        else:
            return cpu.registers.read_register(src)

    @staticmethod
    def set_data(dst: np.ubyte, data: np.ushort, cpu):
        if DataSrcDst(dst) == DataSrcDst.M:
            cpu.memory.write_byte(cpu.registers.read_register(DataSrcDst.HL), data)
        else:
            cpu.registers.write_register(dst, data)
