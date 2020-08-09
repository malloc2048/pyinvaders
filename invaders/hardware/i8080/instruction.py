from invaders.hardware.i8080.operations.operation import Operation


class Instruction(object):
    def __init__(self):
        self.size = 0
        self.cycles = 0
        self.opcode = 0
        self.mnemonic = ''
        self.operation = Operation()
