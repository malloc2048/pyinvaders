from common.config import Config


if __name__ == '__main__':
    cfg = Config()
    cfg.load(filename='../roms/invaders.cfg')

    if cfg.get_bool("LogEnable"):
        print('true')
    else:
        print('false')
