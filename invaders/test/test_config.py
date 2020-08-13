import logging
import unittest
from common.config import Config


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
        self.cfg = Config()

    def test_load(self):
        self.cfg.load('not_a_file')
        self.assertEqual(0, len(self.cfg.items))

        self.cfg.load('../../roms/invaders.cfg')
        self.assertNotEqual(0, len(self.cfg.items))
        self.assertFalse(self.cfg.get_bool('log_enable'))
        self.assertEqual('../roms/instruction_set.csv', self.cfg.get_string('instruction_set'))

    def test_get_not_a_key(self):
        self.assertFalse(self.cfg.get_bool('not_a_key'))
        self.assertEqual('', self.cfg.get_string('not_a_key'))
