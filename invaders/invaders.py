import ctypes
import logging
from sdl2 import *
import numpy as np
from common import *
from hardware import *


class Invaders(object):
    def __init__(self, cfg: Config):
        self.timer = np.uint(0)
        self.cfg = cfg
        self.should_quit = False
        self.cabinet = Cabinet(self.cfg)

        self.window = None
        self.texture = None
        self.renderer = None

        self.initialized = self.window_init() & self.hardware_init()
        self.update_screen()

    def run(self):
        self.timer = SDL_GetTicks()
        while not self.should_quit:
            self.main_loop()

    def main_loop(self):
        self.poll_event()

        if SDL_GetTicks() - (self.timer > (1.0 / FPS) * 1000):
            self.timer = SDL_GetTicks()
            self.game_update()
            self.gpu_update()

        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)

    def gpu_update(self):
        for i in range(0, int((ScreenWidth * ScreenHeight) / 8)):
            y = int(i * 8 / ScreenHeight)
            base_x = (i * 8) % ScreenHeight
            current_byte = self.cabinet.memory.read_byte(VRAMAddress + i)

            for bit in range(0, 8):
                px = base_x + bit
                py = y
                is_lit = (current_byte >> bit) & 1

                red = np.ubyte(0)
                blue = np.ubyte(0)
                green = np.ubyte(0)

                if is_lit:
                    red = 0
                    blue = 0
                    green = 255

                temp_x = px
                px = py
                py = -temp_x + ScreenHeight - 1

                self.cabinet.screen_buffer[py][px][0] = red
                self.cabinet.screen_buffer[py][px][1] = green
                self.cabinet.screen_buffer[py][px][2] = blue

        self.update_screen()

    def window_init(self) -> bool:
        SDL_Init(SDL_INIT_VIDEO)

        self.window = SDL_CreateWindow(
            b"Space Invaders", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
            ScreenWidth * 2, ScreenHeight * 2, SDL_WINDOW_RESIZABLE)

        if self.window is None:
            logging.error('unable to create game window: {}'.format(SDL_GetError()))
            return False

        SDL_SetWindowMinimumSize(self.window, ScreenWidth, ScreenHeight)
        SDL_ShowCursor(SDL_DISABLE)

        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        if self.renderer is None:
            logging.error('unable to create render: {}'.format(SDL_GetError()))
            return False
        SDL_RenderSetLogicalSize(self.renderer, ScreenWidth, ScreenHeight)

        renderer_info = SDL_RendererInfo()
        SDL_GetRendererInfo(self.renderer, renderer_info)
        logging.info("using renderer: {}".format(renderer_info.name))

        self.texture = SDL_CreateTexture(
            self.renderer, SDL_PIXELFORMAT_RGBA32, SDL_TEXTUREACCESS_STREAMING, ScreenWidth, ScreenHeight)
        if self.texture is None:
            logging.error("unable to create texture: {}".format(SDL_GetError()))
            return False
        return True

    def poll_event(self):
        event = SDL_Event()
        while SDL_PollEvent(event) > 0:
            if event.type == SDL_QUIT:
                self.should_quit = True
            elif event.type == SDL_KEYUP:
                self.handle_key_up(event.key.keysym.scancode)
            elif event.type == SDL_KEYDOWN:
                self.handle_key_down(event.key.keysym.scancode)

    def game_update(self):
        cycle_count = 0
        while cycle_count <= CyclesPerFrame:
            start_cycle = self.cabinet.get_cycle_count()
            opcode = self.cabinet.memory.read_byte(self.cabinet.get_program_counter())

            self.cabinet.cpu.step()
            cycle_count += self.cabinet.get_cycle_count() - start_cycle

            if opcode == 0xdb:
                self.handle_in()
            elif opcode == 0xd3:
                self.handle_out()

            if self.cabinet.get_cycle_count() >= HalfCyclesPerFrame:
                self.cabinet.interrupt(np.ushort(self.cabinet.next_interrupt))
                self.cabinet.set_cycle_count(self.cabinet.get_cycle_count() - HalfCyclesPerFrame)

                if self.cabinet.next_interrupt == 0x08:
                    self.cabinet.next_interrupt = 0x10
                elif self.cabinet.next_interrupt == 0x10:
                    self.cabinet.next_interrupt = 0x08

    def hardware_init(self) -> bool:
        self.cabinet.port1 = 1 << 3
        self.cabinet.port2 = 0
        return True

    def update_screen(self):
        pitch = 4 * ScreenWidth
        pointer = ctypes.cast(c_char_p(bytes(self.cabinet.screen_buffer)), ctypes.c_void_p)
        SDL_UpdateTexture(self.texture, None, pointer, pitch)

    def handle_in(self):
        port = self.cabinet.cpu.next_byte()
        if port == 1:
            self.cabinet.set_accumulator(self.cabinet.port1)
        elif port == 2:
            self.cabinet.set_accumulator(self.cabinet.port2)
        elif port == 3:
            shift_val = self.cabinet.shift1 << 8 | self.cabinet.shift0
            self.cabinet.set_accumulator((shift_val >> (8 - self.cabinet.shift_offset)) & 0xff)

    def handle_out(self):
        port = self.cabinet.cpu.next_byte()
        if port == 2:
            self.cabinet.shift_offset = self.cabinet.get_accumulator() & 0x07
        elif port == 3:
            pass # used for sound maybe add later
        elif port == 4:
            self.cabinet.shift0 = self.cabinet.shift1
            self.cabinet.shift1 = self.cabinet.get_accumulator()
        elif port == 5:
            pass # used for sound maybe add later

    def handle_key_up(self, scancode: SDL_Scancode):
        if scancode == SDL_SCANCODE_ESCAPE:
            self.should_quit = True
        elif scancode == SDL_SCANCODE_T:
            self.cabinet.port2 &= 0xfb
        elif scancode == SDL_SCANCODE_C:
            self.cabinet.port1 &= 0xfe
        elif scancode == SDL_SCANCODE_A or scancode == SDL_SCANCODE_LEFT:
            self.cabinet.port1 &= 0xdf
        elif scancode == SDL_SCANCODE_D or scancode == SDL_SCANCODE_RIGHT:
            self.cabinet.port1 &= 0xbf
        elif scancode == SDL_SCANCODE_W or scancode == SDL_SCANCODE_SPACE:
            self.cabinet.port1 &= 0xef
        elif scancode == SDL_SCANCODE_RETURN:
            self.cabinet.port1 &= 0xfb

    def handle_key_down(self, scancode: SDL_Scancode):
        if scancode == SDL_SCANCODE_ESCAPE:
            self.should_quit = True
        elif scancode == SDL_SCANCODE_T:
            self.cabinet.port2 |= 0x04
        elif scancode == SDL_SCANCODE_C:
            self.cabinet.port1 |= 0x01
        elif scancode == SDL_SCANCODE_A or scancode == SDL_SCANCODE_LEFT:
            self.cabinet.port1 |= 0x20
        elif scancode == SDL_SCANCODE_D or scancode == SDL_SCANCODE_RIGHT:
            self.cabinet.port1 |= 0x40
        elif scancode == SDL_SCANCODE_W or scancode == SDL_SCANCODE_SPACE:
            self.cabinet.port1 |= 0x10
        elif scancode == SDL_SCANCODE_RETURN:
            self.cabinet.port1 |= 0x04


if __name__ == '__main__':
    cfg = Config()
    cfg.load(filename='../roms/invaders.cfg')

    logging.basicConfig(filename=cfg.get_string('log_filename'), filemode='w', format='%(message)s', level=logging.DEBUG)
    # logging.basicConfig(filename=cfg.get_string('log_filename'), filemode='w',
    #                     format='%(levelname)s - %(message)s', level=logging.DEBUG)

    game = Invaders(cfg)
    game.run()
