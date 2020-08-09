from enum import Enum


class DataSrcDst(Enum):
    B = 0
    C = 1
    D = 2
    E = 3
    H = 4
    L = 5
    M = 6
    A = 7
    BC = 8
    DE = 9
    HL = 10
    SP = 11


FPS = 60
ScreenWidth = 224
ScreenHeight = 256
VRAMAddress = 0x2400
CyclesPerFrame = 2000000 / FPS
ConfigFilename = '../rom/invaders.cfg'
HalfCyclesPerFrame = CyclesPerFrame / 2
