from help import CellType, Line
from typing import Tuple, List


class Canvas:
    def __init__(self, width: int, height: int) -> None:
        assert width > 0
        assert height > 0
        
        self.width = width
        self.height = height
        self.cells = [[CellType.empty]*width for i in range(height)]
    
    def __getitem__(self, position: Tuple[int, int]) -> CellType:
        y, x = position
        return self.cells[y][x]
    
    def __setitem__(self, position: Tuple[int, int], value: CellType) -> None:
        y, x = position
        self.cells[y][x] = value
    
    def __str__(self):
        return '\n'.join(['%d '*self.width % tuple([cell.value \
                                                    for cell in row]) \
                          for row in self.cells])
    
    def add_lines(self, lines: List[Line]) -> None:
        self.lines = lines
    
    def cell_on_edge(self, x: int, y: int) -> bool:
        return (x == 0) or \
               (y == 0) or \
               (x == self.width-1) or \
               (y == self.height-1)
    
    def empty_cells_among_neighbors(self, x: int, y: int) -> bool:
        neighbors = [(x, y-1), (x-1, y), (x, y+1), (x+1, y)]
        
        return any(self[n] == CellType.empty for n in neighbors)
    
    def draw_line(self, line: Line) -> None:
        # The function rasterizes the line by selecting points
        # with integer coordinates that best obey the equation of the line.
        
        x0, y0, x1, y1 = map(int, (*line[0], *line[1]))
        x, y = x0, y0
        
        dx = 2*(x1 > x0) - 1
        dy = 2*(y1 > y0) - 1

        while True:
            self[(x, y)] = CellType.filled
            
            if x == x1 and y == y1:
                break
                
            errx = abs((y1 - y0)*(x+dx-x0) + (y0 - y)*(x1 - x0))
            erry = abs((y1 - y0)*(x-x0) + (y0 - y-dy)*(x1 - x0))
            
            x += (errx < erry)*dx
            y += (errx >= erry)*dy

    def fill_holes(self) -> None:
        # The function fills closed contours in the 'cellular automata' style:
        # any cell adjacent to empty ones becomes empty.
        # The cell pointer moves in a spiral from the top left corner
        # to the center of the canvas. Thanks to this, pouring does not
        # require multiple passes across the canvas.
        
        borders = [-1, -1, self.width, self.height] # left, top, right, bottom
        coord = [0, 0] # start from upper left corner
        steps = [1, 1, -1, -1] # l->r, t->b, r->l, b->t
        
        # first we move to the right
        coord_idx = 0 # for this reason, we change the X coordinate first
        border_idx = 2 # accordingly, we check the right border
        step_idx = 0 # left->right step
        
        # first mark all empty cells
        self.cells = [[CellType.marked if cell == CellType.empty \
                                       else cell \
                                       for cell in row] \
                                       for row in self.cells]
        
        while True:
            # sequentially clear all marked cells
            # if they are on the edge of the canvas or adjacent to empty ones
            if self[coord] == CellType.marked and \
               (self.cell_on_edge(coord[0], coord[1]) or \
                self.empty_cells_among_neighbors(coord[0], coord[1])):
                   self[coord] = CellType.empty
            
            coord[coord_idx] += steps[step_idx]
            
            # if we come across a border, we shift it in the direction
            # opposite to the movement (for the next loop of the spiral)
            # and turn clockwise
            if coord[coord_idx] + steps[step_idx] == borders[border_idx]:
                borders[border_idx] += -steps[step_idx]
                
                coord_idx = (coord_idx + 1) % len(coord)
                step_idx = (step_idx + 1) % len(steps)
                border_idx = (border_idx + 1) % len(borders)
                
                # if after turning we hit the border again,
                # the center of the canvas has been reached
                if coord[coord_idx] + steps[step_idx] == borders[border_idx]:
                    break
        
        # if there are marked cells left at the end, paint them over
        self.cells = [[CellType.filled if cell == CellType.marked \
                                       else cell \
                                       for cell in row] \
                                       for row in self.cells]
