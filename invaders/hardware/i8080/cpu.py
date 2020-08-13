import logging
import binascii
import numpy as np
from common.config import Config
from hardware.memory import Memory
from hardware.i8080.flags import Flags
from hardware.i8080.operations import *
from hardware.i8080.registers import Registers
from hardware.i8080.instruction import Instruction


class CPU(object):
    def __init__(self, memory: Memory, cfg: Config, flags: Flags):
        self.cfg = cfg
        self.memory = memory
        self.instructions = dict()

        self.flags = flags
        self.cycles = np.uint(0)
        self.registers = Registers()

        self.operations_map = {
            "machine": Machine(),
            "logical": Logical(),
            "branch": Branching(),
            "transfer": DataTransfer(),
            "arithmetic": Arithmetic()
        }

    def step(self):
        address = self.registers.program_counter
        opcode = self.next_byte()
        if self.cfg.get_bool("log_enable"):
            if address == 0x0000:
                print('Reset')
            elif address == 0x18d4:
                print('Initializiation')
            elif address == 0x01e6:
                print('Copy ROM to RAM')
            elif address == 0x18dc:
                print('DrawStatus')
            elif address == 0x1a5c:
                print('ClearScreen')
            elif address == 0x191a:
                print('DrawScoreHead')
            elif address == 0x08f3:
                print('PrintMessage')
            elif address == 0x08ff:
                print('DrawChar')
            elif address == 0x1439:
                print('DrawSimpleSprite')

            # logging.info('Opcode: {:02x}\tprogram counter: {:04x}'.format(opcode, address))
            # print('Opcode: {:02x}\tprogram counter: {:04x}'.format(opcode, address))
            # logging.info('Opcode: {:02x} Registers: {} Flags: {}'.format(opcode, self.registers, self.flags))

        try:
            self.cycles += self.instructions[opcode].cycles
            self.instructions[opcode].operation.execute(opcode, self)
        except KeyError:
            if opcode is None:
                logging.warning('cpu type error')
            else:
                logging.warning('unknown opcode: {}'.format(hex(opcode)))

    def load_instruction_set(self):
        with open(self.cfg.get_string('instruction_set')) as instruction_set:
            lines = instruction_set.readlines()
            for line in lines:
                line = line.strip()
                tokens = line.split(':')
                if len(tokens) == 5:
                    self.make_instruction(tokens)
            instruction_set.close()

    def make_instruction(self, tokens: list):
        opcode = np.ubyte(ord(binascii.unhexlify(tokens[0])))
        try:
            size = np.ubyte(tokens[2])
        except ValueError:
            size = 0

        try:
            cycles = np.uint(tokens[3])
        except ValueError:
            cycles = 0

        try:
            operation = self.operations_map[tokens[4]]
        except KeyError:
            operation = None

        self.instructions[opcode] = Instruction(
            size, cycles, opcode, tokens[1], operation
        )

    def next_byte(self) -> np.ubyte:
        data = self.memory.read_byte(self.registers.program_counter)
        self.registers.program_counter += 1

        if data is None:
            logging.warning('WTF')
        return data
