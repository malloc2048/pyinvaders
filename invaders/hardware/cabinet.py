import numpy as np
from common.config import Config
from hardware.memory import Memory
from hardware.i8080.cpu import CPU
from hardware.i8080.flags import Flags


class Cabinet(object):
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.flags = Flags()
        self.memory = Memory()
        self.cpu = CPU(self.memory, self.cfg, self.flags)

        self.cpu.load_instruction_set()
        self.memory.load_rom(cfg.get_string('rom_filename'))

        self.next_interrupt = np.ubyte(0x08)
        self.screen_buffer = np.zeros((256, 224, 4))

        self.shift0 = np.ubyte(0)
        self.shift1 = np.ubyte(0)
        self.port1 = np.ubyte(0x08)
        self.port2 = np.ubyte(0x03)
        self.shift_offset = np.ubyte(0)

    def get_program_counter(self) -> np.ushort:
        return self.cpu.registers.program_counter

    def get_cycle_count(self) -> np.uint:
        return self.cpu.cycles

    def interrupt(self, address: np.ushort):
        if self.flags.interrupt_enabled:
            self.flags.interrupt_enabled = False

            self.cpu.registers.stack_pointer -= 2
            self.memory.write_word(self.cpu.registers.stack_pointer, self.cpu.registers.program_counter)

            self.cpu.registers.program_counter = address
            self.cpu.cycles += 11

    def set_cycle_count(self, count: np.ushort):
        self.cpu.cycles = count

    def get_accumulator(self) -> np.ubyte:
        return self.cpu.registers.accumulator

    def set_accumulator(self, value: np.ubyte):
        self.cpu.registers.accumulator = value

    def increment_program_counter(self, increment: np.ubyte):
        self.cpu.registers.program_counter += increment
