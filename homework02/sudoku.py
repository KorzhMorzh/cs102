def read_sudoku(filename) -> list:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def group(values: list, n: int) -> list:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    l = [[0 for j in range(n)] for i in range(n)]
    index = 0
    for i in range(n):
        for j in range(n):
            l[i][j] = values[index]
            index += 1
    return l

