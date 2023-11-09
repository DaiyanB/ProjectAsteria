def foo(var, *args):
    print(var)
    if args:
        print('args', args)

foo(5, 1)