from Slicer import Slicer
from OBJGeometry import OBJGeometry



if __name__ == "__main__":
    geometry = OBJGeometry('test.obj')
    slicer = Slicer(geometry, dots_per_side = 16)
    layers = slicer.slice(thickness = 1.0)
    for lay in layers:
        str = lay.__str__()
        print(str)