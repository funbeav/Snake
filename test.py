class A:
    def __init__(self):
        print('a')

class B(A):
    def __init__(self):
        super(B, self).__init__()
        print('b')

b = B()