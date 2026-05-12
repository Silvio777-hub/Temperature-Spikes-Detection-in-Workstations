import unittest
import time
import multiprocessing as mp
from src.stress import cpu_stress, memory_stress

class TestStress(unittest.TestCase):
    def test_cpu_stress_duration(self):
        start = time.time()
        # Run small stress test
        cpu_stress(duration=1, workers=1)
        end = time.time()
        self.assertGreaterEqual(end - start, 1)

    def test_memory_stress(self):
        # Just check it doesn't crash
        memory_stress(duration=1, size_mb=10)

if __name__ == '__main__':
    unittest.main()
