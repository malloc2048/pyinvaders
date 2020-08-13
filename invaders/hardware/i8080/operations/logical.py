import numpy as np
from hardware.i8080.operations.operation import Operation


class Logical(Operation):
    def __init__(self):
        super().__init__()

    def execute(self, opcode: np.ubyte, cpu):
        if (opcode & 0xf8) == 0xa0:
            self.ana(self.get_data(opcode & 0x07, cpu), cpu)
        elif opcode == 0xe6:
            self.ana(self.next_byte(cpu), cpu)
            cpu.flags.half_carry = False
        elif opcode & 0xf8 == 0xa8:
            self.xra(self.get_data(opcode & 0x07, cpu), cpu)
        elif opcode == 0xee:
            self.xra(self.next_byte(cpu), cpu)
        elif opcode & 0xf8 == 0xb0:
            self.ora(self.get_data(opcode & 0x07, cpu), cpu)
        elif opcode == 0xf6:
            self.ora(self.next_byte(cpu), cpu)
        elif (opcode & 0xf8) == 0xb8:
            self.compare(self.get_data(opcode & 0x07, cpu), cpu)
        elif opcode == 0xfe:
            self.compare(self.next_byte(cpu), cpu)
        elif opcode == 0x07:
            carry = cpu.registers.accumulator >> 7
            cpu.flags.carry = False
            if carry > 0:
                cpu.flags.carry = True
            cpu.registers.accumulator = cpu.registers.accumulator << 0x01
            if carry > 0:
                cpu.registers.accumulator |= 0x01
        elif opcode == 0x0f:
            cpu.flags.carry = cpu.registers.accumulator & 0x01
            if cpu.flags.carry:
                cpu.registers.accumulator = cpu.registers.accumulator >> 0x01 | 0x80
            else:
                cpu.registers.accumulator = cpu.registers.accumulator >> 0x01
        elif opcode == 0x17:
            if cpu.flags.carry:
                carry = 0x01
            else:
                carry = 0x00
            cpu.flags.carry = (cpu.registers.accumulator >> 7) > 0
            cpu.registers.accumulator = (cpu.registers.accumulator << 1) | carry
        elif opcode == 0x1f:
            if cpu.flags.carry:
                carry = 0x80
            else:
                carry = 0x00
            cpu.flags.carry = cpu.registers.accumulator & 1 > 0
            cpu.registers.accumulator = (cpu.registers.accumulator >> 1) | carry
        elif opcode == 0x2f:
            cpu.registers.accumulator ^= 0xff
        elif opcode == 0x3f:
            cpu.flags.carry = not cpu.flags.carry
        elif opcode == 0x37:
            cpu.flags.carry = True

    def ana(self, data, cpu):
        accumulator = cpu.registers.accumulator
        cpu.registers.accumulator &= data

        cpu.flags.zero = cpu.registers.accumulator == 0
        cpu.flags.sign = cpu.registers.accumulator > 0x7f
        cpu.flags.calculate_parity(cpu.registers.accumulator)
        cpu.flags.carry = False
        cpu.flags.half_carry = ((cpu.registers.accumulator | accumulator) & 0x08) != 0
    
    def xra(self, data, cpu):
        result = cpu.registers.accumulator ^ data

        cpu.flags.zero = result == 0
        cpu.flags.sign = result > 0x7f
        cpu.flags.calculate_parity(result)
        cpu.flags.carry = False
        cpu.flags.half_carry = False
        cpu.registers.accumulator = result & 0x00ff
    
    def ora(self, data, cpu):
        result = cpu.registers.accumulator | data

        cpu.flags.zero = result == 0
        cpu.flags.sign = result > 0x7f
        cpu.flags.calculate_parity(result)
        cpu.flags.carry = False
        cpu.flags.half_carry = False
        cpu.registers.accumulator = result & 0x00ff
    
    def compare(self, data, cpu):
        result = cpu.registers.accumulator - data

        cpu.flags.zero = result == 0
        cpu.flags.sign = (result & 0x00ff) > 0x7f
        cpu.flags.calculate_parity(result)
        cpu.flags.carry = (result & 0x0100) != 0
        cpu.flags.half_carry = (result & 0x000f) > (cpu.registers.accumulator & 0x0f)
