import numpy as np
from common.constants import DataSrcDst
from hardware.i8080.operations.operation import Operation


class Arithmetic(Operation):
    def execute(self, opcode: np.ubyte, cpu):
        if opcode & 0xf8 == 0x80:
            self.add(self.get_data(opcode & 0x07, cpu), cpu)
        elif 0x88 <= opcode <= 0x8f:
            if cpu.flags.carry:
                self.add(self.get_data(opcode & 0x07, cpu) + 0x01, cpu)
            else:
                self.add(self.get_data(opcode & 0x07, cpu),cpu)
        elif opcode == 0xc6:
            self.add(self.next_byte(cpu), cpu)
        elif opcode == 0xce:
            if cpu.flags.carry:
                self.add(self.next_byte(cpu) + 0x01, cpu)
            else:
                self.add(self.next_byte(cpu), cpu)
        elif 0x90 <= opcode <= 0x97:
            self.subtract(self.get_data(opcode & 0x07, cpu), cpu)
        elif 0x98 <= opcode <= 0x9f:
            if cpu.flags.carry:
                self.subtract(self.get_data(opcode & 0x07, cpu) + 0x01, cpu)
            else:
                self.subtract(self.get_data(opcode & 0x07, cpu), cpu)
        elif opcode == 0xd6:
            self.subtract(self.next_byte(cpu), cpu)
        elif opcode == 0xde:
            if cpu.flags.carry:
                self.subtract(self.next_byte(cpu) + 0x01, cpu)
            else:
                self.subtract(self.next_byte(cpu), cpu)
        elif (opcode & 0xC7) == 0x04:
            self.increment((opcode & 0x38) >> 3, cpu)
        elif (opcode & 0xCF) == 0x03:
            reg = ((opcode & 0x30) >> 4) + 8
            data = self.get_data(reg, cpu) + 1
            self.set_data(reg, data, cpu)
        elif opcode == 0x3d:
            reg = (opcode & 0x38) >> 3
            self.decrement(np.ubyte(7), cpu)
        elif (opcode & 0xc7) == 0x05:
            reg = (opcode & 0x38) >> 3
            self.decrement((opcode & 0x38) >> 3, cpu)
        elif (opcode & 0xCF) == 0x0b:
            reg = ((opcode & 0x30) >> 4) + 8
            data = self.get_data(reg, cpu) - 1
            self.set_data(reg, data, cpu)
        elif (opcode & 0xCF) == 0x09:
            self.dad(((opcode & 0x30) >> 4) + 8, cpu)
        elif opcode == 0x27:
            self.daa(cpu)

    def add(self, data: np.ubyte, cpu):
        sum = np.ushort(data) + np.ushort(cpu.registers.accumulator)

        cpu.flags.zero = (sum & 0xff) == 0
        cpu.flags.sign = (sum & 0xff) > 0x007f
        cpu.flags.calculate_parity(sum)
        cpu.flags.carry = (sum & 0x100) != 0
        cpu.flags.half_carry = (cpu.registers.accumulator & 0x0f) > (sum & 0x000f)

        cpu.registers.accumulator = sum & 0x00ff

    def subtract(self, data: np.ubyte, cpu):
        diff = cpu.registers.accumulator - data

        cpu.flags.half_carry = (diff & 0x000f) > (cpu.registers.accumulator & 0x0f)
        cpu.flags.zero = (diff & 0xff) == 0
        cpu.flags.sign = (diff & 0xff) > 0x007f
        cpu.flags.calculate_parity(diff)
        cpu.flags.carry = (diff & 0x100) != 0

        cpu.registers.accumulator = diff & 0x00ff

    def increment(self, dst: np.ubyte, cpu):
        value = self.get_data(dst, cpu) + 1

        cpu.flags.zero = (value & 0xff) == 0
        cpu.flags.sign = (value & 0xff) > 0x007f
        cpu.flags.calculate_parity(value)
        cpu.flags.half_carry = (cpu.registers.accumulator & 0x0f) > (value & 0x000f)
        self.set_data(dst, value, cpu)

    def decrement(self, dst: np.ubyte, cpu):
        value = self.get_data(dst, cpu) - 1

        cpu.flags.zero = (value & 0xff) == 0
        cpu.flags.sign = (value & 0xff) > 0x007f
        cpu.flags.calculate_parity(value)
        cpu.flags.half_carry = (value & 0x0f) == 0x000f
        self.set_data(dst, value, cpu)

    def dad(self, src: np.ubyte, cpu):
        sum = self.get_data(src, cpu) + self.get_data(np.uint8(10), cpu)
        cpu.flags.carry = (sum & 0x10000) != 0
        self.set_data(np.uint8(10), sum, cpu)

    def daa(self, cpu):
        lsb = cpu.registers.accumulator & 0x0f

        if cpu.flags.half_carry or lsb > 9:
            cpu.registers.accumulator += 6

        msb = cpu.registers.accumulator >> 4
        if cpu.flags.carry or msb > 9:
            msb += 6
        cpu.registers.accumulator &= 0x0f
        cpu.registers.accumulator |= msb << 0x04

        cpu.flags.zero = (cpu.registers.accumulator & 0xff) == 0
        cpu.flags.sign = (cpu.registers.accumulator & 0xff) > 0x007f
        cpu.flags.calculate_parity(cpu.registers.accumulator)
        cpu.flags.half_carry = (lsb & 0x10) != 0
        cpu.flags.carry = msb > 9
