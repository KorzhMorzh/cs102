class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


def createTree():
    root = Tree()
    root.data = 1
    root.left = Tree()
    root.left.data = 2
    root.right = Tree()
    root.right.data = 3

    root.left.left = Tree()
    root.left.left.data = 4
    root.left.right = Tree()
    root.left.right.data = 5
    root.right.left = Tree()
    root.right.left.data = 6
    root.right.right = Tree()
    root.right.right.data = 7
    return root


def compute(tree):
    


tree = createTree()
print(compute(tree))
print(tree)
