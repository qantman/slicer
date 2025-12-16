from help import Vertice, Triangle
from typing import List


class Geometry:
    def __init__(self, vertices: List[Vertice], triangles: List[Triangle]) -> None:
        self.vertices = vertices
        self.triangles = triangles
    
    def get_boundary(self, axis: str, kind: str) -> float:
        assert axis == 'x' or axis == 'y' or axis == 'z'
        assert kind == 'min' or kind == 'max'
        
        axis_values = {'x': 0, 'y': 1, 'z': 2}
        kind_values = {'min': min, 'max': max}
        
        return kind_values[kind]([v[axis_values[axis]] \
                                  for v in self.vertices])
    
    def prepare(self, factor: float) -> None:
        min_x = self.get_boundary('x', 'min')
        min_y = self.get_boundary('y', 'min')
        min_z = self.get_boundary('z', 'min')
        
        max_x = self.get_boundary('x', 'max')
        max_y = self.get_boundary('y', 'max')
        max_z = self.get_boundary('z', 'max')
        
        maximals = (max_x, max_y, max_z)
        minimals = (min_x, min_y, min_z)
        
        coef = factor/max(map(lambda t: t[0]-t[1],
                              zip(maximals, minimals)))
        
        self.vertices = [tuple(map(lambda t: (t[0]-t[1])*coef + 0.5,
                                   zip(vert, minimals))) \
                         for vert in self.vertices]
