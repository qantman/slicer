from help import CellType, Line, Vertice, Triangle
from typing import Dict, Tuple, List
from Geometry import Geometry
from Canvas import Canvas


class Slicer:
    def __init__(self, geometry: Geometry, dots_per_side: int) -> None:
        assert dots_per_side > 1
        
        self.dots_per_side = dots_per_side
        self.geometry = geometry
        self.geometry.prepare(float(self.dots_per_side-1))

    def slice(self, thickness: float) -> List[Canvas]:
        layers_amount = int(self.geometry.get_boundary('z', 'max')/thickness)
        layers = []
        
        epsilon = 1e-6
        
        for i in range(layers_amount):
            lines = []
            layer_canvas = Canvas(self.dots_per_side,
                                  self.dots_per_side)
            
            current_z = (i + 0.5) * thickness

            for tri in self.geometry.triangles:
                upper_points = []
                lower_points = []
                layer_points = []
                
                triangle = tuple([self.geometry.vertices[v] for v in tri])
                
                for point in triangle:
                    if abs(point[2] - current_z) < epsilon:
                        layer_points += [point]
                    elif point[2] > current_z:
                        upper_points += [point]
                    else:
                        lower_points += [point]
                
                # the triangle does not intersect the plane,
                # there is nothing to do here
                if len(upper_points) == 3 or len(lower_points) == 3:
                    continue
                
                # if one point of the triangle lies in the plane,
                # turn it into a pixel
                if len(layer_points) == 1:
                    lines += [(layer_points[0][:-1],
                               layer_points[0][:-1])]
                    continue
                
                # if the entire triangle or one of its edges lies in the plane,
                # no coordinate transformation is required,
                # send it for drawing directly
                if len(layer_points) >= 2:
                    for i in range(len(layer_points)-1):
                        for j in range(i+1, len(layer_points)):
                            lines += [(layer_points[i][:-1],
                                       layer_points[j][:-1])]
                    continue
                
                # the most difficult case is when a triangle intersects a plane,
                # requiring calculation of the coordinates
                # of the intersection points
                start_point = None
                final_points = []
                
                if len(upper_points) == 2:
                    final_points = upper_points
                    start_point = lower_points[0]
                else:
                    final_points = lower_points
                    start_point = upper_points[0]
                
                # we will calculate the parameters for parametric equations
                # of lines 'start -> final[0]' and 'start -> final[1]',
                # for which the z coordinate is equal to the
                # height of the plane (current_z)
                params = [(current_z - start_point[2])/(p[2] - start_point[2]) \
                          for p in final_points]
                
                lines += [tuple([(start_point[0]*(1-params[i]) + \
                                  final_points[i][0]*params[i],
                                  start_point[1]*(1-params[i]) + \
                                  final_points[i][1]*params[i]) \
                                  for i in range(2)])]
            
            for line in lines:
                layer_canvas.draw_line(line)
            layer_canvas.fill_holes()
            
            layers += [layer_canvas]
        
        return layers