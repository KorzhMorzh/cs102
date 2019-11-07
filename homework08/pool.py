from multiprocessing import Process, Queue
import psutil
import time
import math
import random
import threading


class ProcessPool:
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.max_memory = 0
        self.convert_memory(mem_usage)
        if min_workers > max_workers:
            raise Exception("Минимальное кол-во процессов не "
                            "может быть больше максимального")

    def convert_memory(self, mem_usage):
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
        p = Process(target=func, name='test process', args=(iterable[0],))
        p.start()
        p_m = threading.Thread(target=self.max_memory_usage, name='test mem', args=(p.pid,))
        p_m.start()
        p.join()
        p_m.join()
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
        # begin = time.time()
        length = q.qsize()
        if length <= amount_process:
            amount_process = length
        while not q.empty():
            for _i in range(amount_process):
                data = q.get()
                process = Process(target=func, args=(data,))
                processes.append(process)
                process.start()
                if q.empty():
                    # end = time.time()
                    '''print("Время обработки {} чанков данных {} процессами:"
                          .format(length, amount_process), int(end - begin))'''
                    break
            for process in processes:
                process.join()
                process.terminate()
        return amount_process, self.max_memory

    def max_memory_usage(self, pid):
        p_psutil = psutil.Process(pid)
        mem_list = []
        while psutil.pid_exists(pid):
            try:
                mem_list.append(p_psutil.memory_info().rss // 1000000)
            except:
                pass
            time.sleep(0.01)
        self.max_memory = max(mem_list)


def heavy_computation(data_chunk):
    for i in range(456465):
        data_chunk = math.pow(data_chunk, i) * i
    return data_chunk


if __name__ == '__main__':
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='100mb')
    m = 50
    big_data = [random.randint(-m * m, m * m) for i in range(m)]
    result = pool.map(heavy_computation, big_data)
