from enum import Enum
from enum import Enum
from typing import Tuple

Line = Tuple[Tuple[float, float],
             Tuple[float, float]]

Vertice = Tuple[float, float, float]
Triangle = Tuple[int, int, int]


class CellType(Enum):
    empty = 0
    filled = 1
    marked = 2