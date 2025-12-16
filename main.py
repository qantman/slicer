from src.Slicer import Slicer
from src.OBJGeometry import OBJGeometry

if __name__ == "__main__":
    geometry = OBJGeometry(input("Enter object name or path to object: "))
    slicer = Slicer(geometry, dots_per_side = 16)
    layers = slicer.slice(thickness = 1.0)
    for lay in layers:
        str = lay.__str__()
        print("===============================")
        print(str)
        print("===============================")
