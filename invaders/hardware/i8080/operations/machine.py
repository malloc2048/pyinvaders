import numpy as np
from hardware.i8080.operations.operation import Operation


class Machine(Operation):
    def __init__(self):
        super().__init__()

    def execute(self, opcode: np.ubyte, cpu):
        if opcode == 0xf5:
            self.push(self.get_psw(cpu), cpu)
        elif opcode & 0xcf == 0xc5:
            self.push(self.get_data(((opcode & 0x30) >> 0x04) + 8, cpu), cpu)
        elif opcode == 0xf1:
            self.set_psw(cpu)
        elif opcode & 0xcf == 0xc1:
            self.pop(((opcode & 0x30) >> 0x04) + 8, cpu)
        elif opcode == 0xe3:
            self.xthl(cpu)
        elif opcode == 0xf9:
            cpu.registers.stack_pointer = self.get_data(np.ubyte(10), cpu)
        elif opcode == 0xfb:
            cpu.flags.interrupt_enabled = True
        elif opcode == 0xf3:
            cpu.flags.interrupt_enabled = False
        elif opcode == 0x76:
            cpu.flags.halted = True

    def get_psw(self, cpu) -> np.ushort:
        psw = cpu.registers.accumulator << 8
        psw &= 0xff00

        if cpu.flags.zero: psw |= 0x01
        if cpu.flags.sign: psw |= 0x02
        if cpu.flags.parity: psw |= 0x04
        if cpu.flags.carry: psw |= 0x08
        if cpu.flags.half_carry: psw |= 0x10

        return psw

    def set_psw(self, cpu):
        psw = cpu.memory.read_word(cpu.registers.stack_pointer)
        cpu.registers.stack_pointer += 2

        cpu.registers.accumulator = psw >> 0x08 > 0
        cpu.flags.zero = psw & 0x01 > 0
        cpu.flags.sign = psw & 0x02 > 0
        cpu.flags.parity = psw & 0x04 > 0
        cpu.flags.carry = psw & 0x08 > 0
        cpu.flags.half_carry = psw & 0x10 > 0

    def push(self, data: np.ushort, cpu):
        cpu.registers.stack_pointer -= 2
        cpu.memory.write_word(cpu.registers.stack_pointer, data)

    def pop(self, dst: np.ubyte, cpu):
        data = cpu.memory.read_word(cpu.registers.stack_pointer)
        self.set_data(dst, data, cpu)
        cpu.registers.stack_pointer += 2

    def xthl(self, cpu):
        sp = cpu.memory.read_word(cpu.registers.stack_pointer)
        cpu.memory.write_word(cpu.registers.stack_pointer, self.get_data(np.ubyte(10), cpu))
        self.set_data(np.ubyte(10), sp, cpu)
