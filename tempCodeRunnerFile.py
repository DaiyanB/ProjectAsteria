val = 0
arr = []

def foo(var):
    if var == 0:
        var = 1
    else:
        var = 0

    # or
    
    if var:
        var = 0
    else:
        var = 1

    return var

def bar(var):
    var += 1

    return var % 2