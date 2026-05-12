import unittest
import os
import time
import threading
from src.monitor import start_monitor, write_log

class TestMonitor(unittest.TestCase):
    def test_write_log(self):
        test_csv = "test_log.csv"
        if os.path.exists(test_csv):
            os.remove(test_csv)
        
        write_log(test_csv, "2023-01-01T00:00:00", 50.0, cpu_usage=10.0)
        self.assertTrue(os.path.exists(test_csv))
        
        with open(test_csv, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2) # Header + 1 row
        
        os.remove(test_csv)

    def test_monitor_start_stop(self):
        # We use a very short loop for testing
        config = {'log_path': 'test_monitor.csv', 'monitor_interval_sec': 0.1}
        if os.path.exists('test_monitor.csv'):
            os.remove('test_monitor.csv')
            
        stop_event = threading.Event()
        from src.monitor import monitor_loop
        
        t = threading.Thread(target=monitor_loop, args=(stop_event, config))
        t.start()
        time.sleep(0.3)
        stop_event.set()
        t.join()
        
        self.assertTrue(os.path.exists('test_monitor.csv'))
        os.remove('test_monitor.csv')

if __name__ == '__main__':
    unittest.main()
