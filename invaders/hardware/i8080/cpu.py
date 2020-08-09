
from invaders.common.config import Config
from invaders.hardware.memory import Memory


class CPU(object):
    def __init__(self, memory: Memory, cfg: Config):
        self.cfg = cfg
        self.memory = Memory

    def step(self):
        pass

    def load_instruction_set(self):
        pass

    def make_instruction(self):
        pass

    def next_byte(self):
        pass