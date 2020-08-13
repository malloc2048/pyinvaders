import logging
import distutils.util


class Config(object):
    def __init__(self):
        self.items = dict()

    def load(self, filename: str):
        try:
            with open(filename) as cfgFile:
                lines = cfgFile.readlines()

                for line in lines:
                    tokens = line.split(':')
                    if len(tokens) == 2:
                        self.items[tokens[0]] = tokens[1].strip()
                cfgFile.close()
        except FileNotFoundError:
            logging.error('config file not found {}'.format(filename))

    def get_bool(self, key: str) -> bool:
        try:
            return bool(distutils.util.strtobool(self.items[key]))
        except KeyError:
            return False

    def get_string(self, key: str) -> str:
        try:
            return self.items[key]
        except KeyError:
            return ''
