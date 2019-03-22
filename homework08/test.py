import unittest
from pool import ProcessPool, heavy_computation
import random


class TestPool(unittest.TestCase):
    def data(self):
        m = 50
        big_data = [random.randint(-m * m, m * m) for _i in range(m)]
        return big_data

    def test_amount_of_process(self):
        process_gb = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Gb')
        process_mb = ProcessPool(min_workers=2, max_workers=10, mem_usage='100mb')
        process_kb = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Kb')
        process_b = ProcessPool(min_workers=2, max_workers=10, mem_usage='100b')
        self.assertEqual([1000, 100, 0.001, 0.0001],
                         [process_gb.mem_usage, process_mb.mem_usage,
                          process_kb.mem_usage, process_b.mem_usage])

    def test_overflow_memory(self):
        process = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Kb')
        with self.assertRaises(Exception) as context:
            process.map(heavy_computation, self.data())
        self.assertTrue('Процесс занимает больше памяти, чем возможно'
                        in str(context.exception))

    def test_amount_processes_less_than_min_workers(self):
        process = ProcessPool(min_workers=500, max_workers=510, mem_usage='50mb')
        data = self.data()
        with self.assertRaises(Exception) as context:
            process.map(heavy_computation, data)
        u = 'Количество возможных процессов меньше минимального количества' in str(context.exception)
        self.assertTrue(u)

    def test_incorrect_memory(self):
        with self.assertRaises(Exception) as context:
            ProcessPool(min_workers=2, max_workers=10, mem_usage='1')
        self.assertTrue('Некорректное значение памяти'
                        in str(context.exception))

    def test_max_less_min(self):
        with self.assertRaises(Exception) as context:
            ProcessPool(min_workers=10, max_workers=9, mem_usage='1gb')
        self.assertTrue('Минимальное кол-во процессов не может быть больше максимального'
                        in str(context.exception))