tree = {'1': {'data': '1',
              'left': {
                  '2': {
                      'data': '2',
                      'left': {
                          '4': {
                              'data': '4',
                              'left': None,
                              'right': None
                          }},
                      'right': {
                          '5': {
                              'data': '5',
                              'left': None,
                              'right': None
                          }
                      }}
              },
              'right': {
                  '3': {
                      'data': '3',
                      'left': {
                          '6': {
                              'data': '6',
                              'left': None,
                              'right': None
                          }
                      },
                      'right': {
                          '7': {
                              'data': '7',
                              'left': None,
                              'right': None
                          }
                      }}
              }
              }
        }

summ = 0


def sum_leaves(tree):
    global summ
    try:
        node = list(tree.keys())
        for i in node:
            if tree[str(i)]['left'] is None and tree[str(i)]['right'] is None:
                summ += int(tree[str(i)]['data'])
            sum_leaves(tree[str(i)]['left'])
            sum_leaves(tree[str(i)]['right'])
    except:
        pass


if __name__ == '__main__':
    sum_leaves(tree)
    print(summ)
