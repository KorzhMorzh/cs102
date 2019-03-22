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
                          process_kb.mem_usage, process_b.mem_usage],
                         "Адекватно присваевается память в зависимости от единиц измерений")

    def test_overflow_memory(self):
        process = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Kb')
        with self.assertRaises(Exception) as context:
            process.map(heavy_computation, self.data())
        self.assertTrue('Процесс занимает больше памяти, чем возможно'
                        in str(context.exception), "Ошибка, если максимальная "
                                                   "память больше используемой")

    def test_amount_processes_less_than_min_workers(self):
        process = ProcessPool(min_workers=2, max_workers=10, mem_usage='30mb')
        with self.assertRaises(Exception) as context:
            process.map(heavy_computation, self.data())
        self.assertTrue('Количество возможных процессов меньше минимального количества'
                        in str(context.exception), "Ошибка, если минимальное "
                                                   "количество процессов больше количества возможных")

