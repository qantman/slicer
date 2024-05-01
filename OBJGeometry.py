from Geometry import Geometry


class OBJGeometry(Geometry):
    def __init__(self, filename: str) -> None:
        data = [s.split() \
                for s in open(filename).readlines()]
        
        vertices = []
        triangles = []
        
        for raw_vertice in [s for s in data if s[0] == 'v']:
            assert len(raw_vertice[1:]) == 3
            vertices += [tuple(map(float, raw_vertice[1:]))]
        
        for raw_face in [s for s in data if s[0] == 'f']:
            assert len(raw_face[1:]) == 3
            triangles += [tuple([int(idx.split(sep = '/')[0])-1 \
                          for idx in raw_face[1:]])]
        
        super().__init__(vertices, triangles)