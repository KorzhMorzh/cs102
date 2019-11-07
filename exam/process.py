import multiprocessing
import tree1
import numpy


def worker(tree, return_dict):
    try:
        node = list(tree.keys())
        for i in node:
            if tree[str(i)]['left'] is None and tree[str(i)]['right'] is None:
                return_dict.append(int(tree[str(i)]['data']))
            worker(tree[str(i)]['left'], return_dict)
            worker(tree[str(i)]['right'], return_dict)
    except:
        pass


def process(tree):
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []
    p1 = multiprocessing.Process(target=worker, args=(tree['1']['left'], return_list))
    jobs.append(p1)
    p1.start()
    p2 = multiprocessing.Process(target=worker, args=(tree['1']['right'], return_list))
    jobs.append(p2)
    p2.start()

    for proc in jobs:
        proc.join()
    summ = numpy.sum(return_list)
    return summ


if __name__ == '__main__':
    tree = tree1.tree
    print(process(tree))
