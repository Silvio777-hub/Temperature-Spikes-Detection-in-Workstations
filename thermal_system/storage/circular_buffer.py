from collections import deque
import pandas as pd

class CircularBuffer:
    """Fixed-size buffer for recent samples."""
    def __init__(self, size=100):
        self.buffer = deque(maxlen=size)

    def add(self, sample):
        self.buffer.append(sample)

    def to_df(self):
        return pd.DataFrame(list(self.buffer))

    def is_full(self):
        return len(self.buffer) == self.buffer.maxlen
