from invaders.common.config import Config
from invaders.hardware.memory import Memory
from invaders.hardware.i8080.cpu import CPU


class Cabinet(object):
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.memory = Memory()
        self.cpu = CPU()

        self.nextInterrupt = 0x08
        self.screenBuffer[256][224][4]

        self.port1 = 0x08
        self.port2 = 0x03
        self.shift0 = 0
        self.shift1 = 0
        self.shiftOffset = 0
