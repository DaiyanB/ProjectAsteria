from .constant import Constant

def convert_coordinates(coordinates, inverse=False):
    if inverse:
        return coordinates/Constant.AU * Constant.SCALE
    else:
        return coordinates*Constant.SCALE / Constant.AU