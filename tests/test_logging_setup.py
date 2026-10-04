import logging
import os
import unittest
from unittest import mock

from scripts.logging_setup import configure_logging


class ConfigureLoggingTest(unittest.TestCase):
    def tearDown(self) -> None:
        logging.basicConfig(force=True)

    def test_defaults_to_warning(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            configure_logging()
        self.assertEqual(logging.getLogger().level, logging.WARNING)

    def test_reads_level_from_env_case_insensitively(self) -> None:
        with mock.patch.dict(os.environ, {"LOG_LEVEL": "debug"}):
            configure_logging()
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

    def test_rejects_invalid_level(self) -> None:
        with mock.patch.dict(os.environ, {"LOG_LEVEL": "loud"}), self.assertRaisesRegex(ValueError, "LOUD"):
            configure_logging()


if __name__ == "__main__":
    unittest.main()
