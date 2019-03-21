from multiprocessing import Process, Queue
import psutil
import time
import math
import random


class ProcessPool:
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.max_memory_ = 0

    def map(self, func, iterable):
        processes = []
        amount_process = int(int(self.mem_usage.split('Gb')[0])
                             * 1024 / self.max_memory_)
        if self.max_memory_ > int(self.mem_usage.split('Gb')[0])*1024:
            print("Процесс занимает больше памяти, чем возможно")
            return 0
        if amount_process < self.min_workers:
            print('Количество возможных процессов меньше '
                  'минимального количества')
            return 0
        elif amount_process > self.max_workers:
            amount_process = self.max_workers
        for i in iterable:
            q.put(i)
        begin = time.time()
        length = q.qsize()
        while not q.empty():
            for _i in range(amount_process):
                data = q.get()
                process = Process(target=func, args=(data,))
                processes.append(process)
                process.start()
                if q.empty():
                    end = time.time()
                    print("Время обработки {} чанков данных {} процессами:"
                          .format(length, amount_process), int(end - begin))
                    break
            for process in processes:
                process.join()

    def max_memory(self, func, iterable):
        begin = time.time()
        max_memory_ = 0
        start_memory = psutil.virtual_memory().used
        memory_usage_refresh = .005
        p = Process(target=func, args=(iterable,))
        p.start()
        while 1:
            time.sleep(memory_usage_refresh)
            delta_mem = psutil.virtual_memory().used - start_memory
            if delta_mem > max_memory_:
                max_memory_ = delta_mem
            if not p.is_alive():
                end = time.time()
                p.join()
                print("Время обработки 1 чанка данных одним процессом: ",
                      int(end - begin))
                self.max_memory_ = int(max_memory_ / 1024 / 1024)
                return self.max_memory_


def heavy_computation(data_chunk):
    for i in range(4534545):
        data_chunk = math.pow(data_chunk, i) * i
    return data_chunk


if __name__ == '__main__':
    q = Queue()
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Gb')
    m = 50
    big_data = [random.randint(-m * m, m * m) for i in range(m)]
    pool.max_memory(heavy_computation, max(big_data))
    result = pool.map(heavy_computation, big_data)
