import unittest
from sync_sftp import ceil_to_next_full_minutes


class MyTestCase(unittest.TestCase):
    def test_ceil_to_next_full_minutes(self):
        self.assertEqual(ceil_to_next_full_minutes(52, 5), 3*60)
        self.assertEqual(ceil_to_next_full_minutes(19, 5), 1*60)
        self.assertEqual(ceil_to_next_full_minutes(21, 5), 4*60)
        self.assertEqual(ceil_to_next_full_minutes(50, 5), 0*60)
        self.assertEqual(ceil_to_next_full_minutes(1, 5), 4*60)
        self.assertEqual(ceil_to_next_full_minutes(0, 2), 0*60)
        self.assertEqual(ceil_to_next_full_minutes(1, 2), 1 * 60)
        self.assertEqual(ceil_to_next_full_minutes(3, 2), 1 * 60)


if __name__ == '__main__':
    unittest.main()
