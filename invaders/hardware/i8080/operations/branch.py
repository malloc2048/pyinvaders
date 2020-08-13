import numpy as np
from hardware.i8080.operations.operation import Operation


class Branching(Operation):
    def __init__(self):
        super().__init__()

    def execute(self, opcode, cpu):
        if opcode == 0xc3:
            cpu.registers.program_counter = self.next_word(cpu)
        elif (opcode & 0xc7) == 0xc2:
            address = self.next_word(cpu)
            condition = self.check_condition((opcode & 0x38) >> 0x03, cpu)

            if opcode & 0x0f == 0x02: # negative condition
                if condition == False:
                    cpu.registers.program_counter = address
            elif opcode & 0x0f == 0x0a:
                if condition == True:
                    cpu.registers.program_counter = address

        elif opcode == 0xcd:
            self.call(cpu)
        elif (opcode & 0xc7) == 0xc4:
            if self.check_condition((opcode & 0x38) >> 0x03, cpu):
                self.call(cpu)
            else:
                cpu.registers.program_counter += 2
        elif opcode == 0xc9:
            self.ret(cpu)
        elif (opcode & 0xc7) == 0xc0:
            if self.check_condition((opcode & 0x38) >> 0x03, cpu):
                self.ret(cpu)
        elif (opcode & 0xc7) == 0xc7:
            self.restart((opcode & 0x038) >> 3,cpu)
        elif opcode == 0xe9:
            cpu.registers.program_counter = cpu.registers.readRegister(np.ubyte(10))

    def ret(self, cpu):
        cpu.registers.program_counter = cpu.memory.read_word(cpu.registers.stack_pointer)
        cpu.registers.stack_pointer += 2

    def call(self, cpu):
        address = self.next_word(cpu)
        cpu.registers.stack_pointer -= 2
        cpu.memory.write_word(cpu.registers.stack_pointer, cpu.registers.program_counter)
        cpu.registers.program_counter = address

    def restart(self, restart_num: np.ubyte, cpu):
        cpu.registers.stack_pointer -= 2
        cpu.memory.write_word(cpu.registers.stack_pointer, cpu.registers.program_counter)
        cpu.registers.program_counter = 8 * restart_num

    @staticmethod
    def check_condition(condition, cpu) -> bool:
        if condition == 0 or condition == 1:
            return cpu.flags.zero
        elif condition == 2 or condition == 3:
            return cpu.flags.carry
        elif condition == 4 or condition == 5:
            return cpu.flags.parity
        elif condition == 6 or condition == 7:
            return cpu.flags.sign
        else:
            return False
