def read_sudoku(filename: str) -> list:
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


def display(values: list):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def get_row(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    i = pos[0]
    l = values[i]
    return l


def get_col(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    j = pos[1]
    l = []
    for i in range(len(values)):
        l.append(values[i][j])
    return l


def get_block(values: list, pos: tuple) -> list:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    l = []
    i = pos[0]
    j = pos[1]
    if i < 3:
        for q in range(3):
            if j < 3:
                for w in range(3):
                    l.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    l.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    l.append(values[q][w])
    elif i < 6:
        for q in range(3, 6):
            if j < 3:
                for w in range(3):
                    l.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    l.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    l.append(values[q][w])
    elif i < 9:
        for q in range(6, 9):
            if j < 3:
                for w in range(3):
                    l.append(values[q][w])
            elif j < 6:
                for w in range(3, 6):
                    l.append(values[q][w])
            elif j < 9:
                for w in range(6, 9):
                    l.append(values[q][w])
    return l


def find_empty_positions(grid: list) -> tuple:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    q = -1
    w = -1
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                q = i
                w = j
                break
        if q >= 0 & w >= 0:
            break
    if q >= 0 & w >= 0:
        return q, w
    else:
        return 'Свободных позиций ', 'нет'


def find_possible_values(grid: list, pos: tuple) -> list:
    """ Вернуть множество всех возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzles/puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    possible_values = []
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for i in values:
        if i in row:
            continue
        elif i in col:
            continue
        elif i in block:
            continue
        else:
            possible_values.append(i)
    return possible_values



