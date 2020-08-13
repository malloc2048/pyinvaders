import numpy as np
from common.constants import DataSrcDst
from hardware.i8080.operations.operation import Operation


class DataTransfer(Operation):
    def __init__(self):
        super().__init__()

    def execute(self, opcode: np.ubyte, cpu):
        src = opcode & 0x07
        dst = (opcode & 0x38) >> 0x03
        regPair = ((opcode & 0x30) >> 0x04) + 8

        if opcode >= 0x40 and opcode <= 0x7f:
            self.set_data(dst, self.get_data(src, cpu), cpu)
        elif (opcode & 0xc7) == 0x06:
            self.set_data(dst, self.next_byte(cpu), cpu)
        elif (opcode & 0xcf) == 0x01:
            data = self.next_word(cpu)
            self.set_data(regPair, data, cpu)
        elif opcode == 0x3a:
            cpu.registers.accumulator = cpu.memory.read_byte(self.next_word(cpu))
        elif opcode == 0x32:
            cpu.memory.write_byte(self.next_word(cpu), cpu.registers.accumulator)
        elif opcode == 0x2a:
            address = self.next_word(cpu)
            cpu.registers.l = cpu.memory.read_byte(address)
            cpu.registers.h = cpu.memory.read_byte(address + 1)
        elif opcode == 0x22:
            address = self.next_word(cpu)
            cpu.memory.write(address, self.get_data(np.ubyte(DataSrcDst.L), cpu))
            cpu.memory.write(address + 1, self.get_data(np.ubyte(DataSrcDst.H), cpu))
        elif (opcode & 0xcf) == 0x0a:
            address = self.get_data(regPair, cpu)
            cpu.registers.accumulator = cpu.memory.read_byte(address)
        elif opcode == 0x02 or opcode == 0x12:
            cpu.memory.write(self.get_data(regPair, cpu), cpu.registers.accumulator)
        elif opcode == 0xeb:
            temp = cpu.registers.h
            cpu.registers.h = cpu.registers.d
            cpu.registers.d = temp

            temp = cpu.registers.l
            cpu.registers.l = cpu.registers.e
            cpu.registers.e = temp
