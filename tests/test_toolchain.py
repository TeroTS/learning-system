import sys
import unittest


class ToolchainTest(unittest.TestCase):
    def test_python_version_is_supported(self) -> None:
        self.assertGreaterEqual(sys.version_info[:2], (3, 11))


if __name__ == "__main__":
    unittest.main()
