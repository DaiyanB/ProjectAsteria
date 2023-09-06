c = 55

class Constant:
    k = 5
    def __init__(self):
        self.c = 50

    def printc(self):
        print(c)

    def update_const(self, A):
        self.k = A

class Object:
    def __init__(self) -> None:
        pass

    def printc(self):
        print(Constant.k)

def update_const(k):
    global c 
    c = k

const = Object()

obj = [const]