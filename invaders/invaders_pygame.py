import pygame
from common.constants import *
from common.config import Config
from hardware.memory import Memory


class Invaders:
    def __init__(self, cfg, storage, cabinet):
        self.timer = 0
        self.cfg = cfg
        self.screen = None
        self.running = True
        self.memory = storage
        self.cabinet = cabinet

        self.init_window()

    def run(self):
        self.timer = pygame.time.get_ticks()
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.poll_events()
        if pygame.time.get_ticks() - self.timer > FRAME_TIME:
            self.timer = pygame.time.get_ticks()
            self.game_update()
            self.screen_update()
        pygame.display.flip()

    def game_update(self):
        pass

    def screen_update(self):
        image = pygame.image.load('logo.jpg')

        for offset in range(0, VRAM_SIZE):
            address = VRAMAddress + offset
            self.memory.write_byte(address, 255)

        for offset in range(0, VRAM_SIZE):
            address = VRAMAddress + offset
            x = (offset * 8) % ScreenHeight
            y = int(offset * 8 / ScreenHeight)
            current_byte = self.memory.read_byte(address)

            for bit_pos in range(0, 8):
                pixel_x = x * bit_pos
                pixel_y = y

                is_lit = (current_byte >> bit_pos) & 1
                temp_x = pixel_x
                pixel_x = pixel_y
                pixel_y = -temp_x + ScreenHeight - 1

                if is_lit:
                    self.screen.set_at((pixel_x, pixel_y), (0, 255, 0, 255))

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_t:
                    pass
                elif event.key == pygame.K_c:
                    pass
                elif event.key == pygame.K_RETURN:
                    pass

    def init_window(self):
        pygame.init()
        logo = pygame.image.load('logo.jpg')
        pygame.display.set_icon(logo)
        pygame.display.set_caption('space invaders')
        self.screen = pygame.display.set_mode((ScreenWidth * 2, ScreenHeight * 2))


if __name__ == '__main__':
    config = Config()
    memory = Memory()
    # make registers
    # make flags
    # make cpu
    # make cabinet
    game = Invaders(None, memory, config)
    game.run()
