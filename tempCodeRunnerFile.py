from utils.utils import generator

one = generator()
two = generator()

for i in range(10):
    if not i % 2:
        print('one', next(one))
    else:
        print('two', next(two))