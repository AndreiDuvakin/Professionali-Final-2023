import unittest
from datetime import time

from Библиотека.SF2022User1Lib import Calculations as ca


class LibTimeTest(unittest.TestCase):

    def test_validator_int(self):
        with self.assertRaises(AttributeError):
            ca.available_periods(1, 2, 3, 4, 5)

    def test_validator_str(self):
        with self.assertRaises(TypeError):
            ca.available_periods('1', '1', '1', '1', '1')

    def test_validator_none(self):
        with self.assertRaises(TypeError):
            ca.available_periods()

    def test_bad_time(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)]
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30
        with self.assertRaises(Exception):
            ca.available_periods(list_cansel, list_len_cansel, time_end, time_begin, consultation)

    def test_long_list_attribute(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)] * 3
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30
        with self.assertRaises(IndexError):
            ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation)

    def test_long_time_attribute(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)]
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30000
        self.assertEquals(ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation), '')

    def test_long_time(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)]
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 0.003
        import time as tt
        start_time = tt.time()
        ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation)
        self.assertEquals(round(tt.time() - start_time), second=2)

    def test_str_time(self):
        list_cansel = ['10:00', '11:00', '15:00', '15:30', '16:50']
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30
        with self.assertRaises(AttributeError):
            ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation)

    def test_str_len(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)]
        list_len_cansel = ['60', '30', '10', '10', '40']
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30
        with self.assertRaises(TypeError):
            ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation)

    def test_ok(self):
        list_cansel = [time(hour=10, minute=0), time(hour=11, minute=0), time(hour=15, minute=0),
                       time(hour=15, minute=30),
                       time(hour=16, minute=50)]
        list_len_cansel = [60, 30, 10, 10, 40]
        time_begin = time(hour=8, minute=0)
        time_end = time(hour=18, minute=0)
        consultation = 30
        self.assertEquals(ca.available_periods(list_cansel, list_len_cansel, time_begin, time_end, consultation),
                          "8:00:00-8:30:00\n"
                          "8:30:00-9:00:00\n"
                          "9:00:00-9:30:00\n"
                          "9:30:00-10:00:00\n"
                          "11:30:00-12:00:00\n"
                          "12:00:00-12:30:00\n"
                          "12:30:00-13:00:00\n"
                          "13:00:00-13:30:00\n"
                          "13:30:00-14:00:00\n"
                          "14:00:00-14:30:00\n"
                          "14:30:00-15:00:00\n"
                          "15:40:00-16:10:00\n"
                          "16:10:00-16:40:00\n"
                          "17:30:00-18:00:00\n")


if __name__ == '__main__':
    unittest.main()
