import unittest
import process
import tree1


class Test(unittest.TestCase):
    def data(self):
        tree = {'1': {'data': '1',
              'left': {
                  '2': {
                      'data': '2',
                      'left': None,
                      'right': None}
              },
              'right': {
                  '3': {
                      'data': '3',
                      'left': None,
                      'right': None}
              }
              }
        }
        return tree

    def test_sum(self):
        tree = self.data()
        tree1.sum_leaves(tree)
        self.assertEqual(5, tree1.summ)

    def test_process(self):
        tree = self.data()
        summ = process.process(tree)
        self.assertEqual(5, summ)


