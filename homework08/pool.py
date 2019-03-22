from multiprocessing import Process, Queue
import psutil
import time
import math
import random


class ProcessPool:
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.max_memory = 0
        if min_workers > max_workers:
            raise Exception("Минимальное кол-во процессов не "
                            "может быть больше максимального")
        if ('gb' in mem_usage.lower()) or ('mb' in mem_usage.lower()) \
                or ('kb' in mem_usage.lower()) or ("b" in mem_usage.lower()):
            try:
                self.mem_usage = int(mem_usage.lower().split('gb')[0]) * 1000
            except ValueError:
                try:
                    self.mem_usage = int(mem_usage.lower().split('mb')[0])
                except ValueError:
                    try:
                        self.mem_usage = int(mem_usage.lower().split('kb')[0]) / 1000
                    except ValueError:
                        self.mem_usage = int(mem_usage.lower().split('b')[0]) / 1000 / 1000
        else:
            raise Exception("Некорректное значение памяти")

    def map(self, func, iterable):
        q = Queue()
        begin = time.time()
        max_memory_ = 0
        start_memory = psutil.virtual_memory().used
        memory_usage_refresh = .005
        p = Process(target=func, args=(max(iterable),))
        p.start()
        while 1:
            time.sleep(memory_usage_refresh)
            delta_mem = psutil.virtual_memory().used - start_memory
            if delta_mem > max_memory_:
                max_memory_ = delta_mem
            if not p.is_alive():
                end = time.time()
                p.join()
                p.terminate()
                print("Время обработки 1 чанка данных одним процессом: ",
                      int(end - begin))
                self.max_memory = int(max_memory_ / 1000 / 1000)
                break
        processes = []
        amount_process = int(self.mem_usage / self.max_memory)
        if self.max_memory > self.mem_usage:
            raise Exception("Процесс занимает больше памяти, чем возможно")
        if amount_process < self.min_workers:
            raise Exception('Количество возможных процессов меньше минимального количества')
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
                process.terminate()


def heavy_computation(data_chunk):
    for i in range(4534545):
        data_chunk = math.pow(data_chunk, i) * i
    return data_chunk


if __name__ == '__main__':
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='100mb')
    m = 50
    big_data = [random.randint(-m * m, m * m) for i in range(m)]
    result = pool.map(heavy_computation, big_data)
