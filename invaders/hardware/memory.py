import logging
# import numpy as np


class Memory(object):
    def __init__(self):
        self.rom_size = 0x2000
        self.rom = [0 for _ in range(self.rom_size)]
        self.ram = [0 for _ in range(0x10000)]

    def load_rom(self, rom_filename: str):
        try:
            with open(rom_filename, 'rb') as rom:
                self.rom = rom.read(self.rom_size)
        except FileNotFoundError:
            logging.error('rom file not found {}'.format(rom_filename))

    def read_byte(self, address: int) -> int:
        try:
            if address < self.rom_size:
                return self.rom[address]
            else:
                return self.ram[address - self.rom_size]
        except IndexError:
            logging.warning('address out of memory range {}'.format(hex(address)))
        except TypeError:
            if address is None:
                logging.warning('type error address is None ')

    def read_word(self, address: int) -> int:
        return self.read_byte(address) | self.read_byte(address + 1) << 0x08

    def write_byte(self, address: int, data: int):
        if address >= self.rom_size:
            self.ram[address - self.rom_size] = data
        else:
            logging.warning('attempt to write to ROM {}'.format(hex(address)))

    def write_word(self, address: int, data: int):
        self.write_byte(address, data)
        self.write_byte(address + 1, data >> 0x08)
