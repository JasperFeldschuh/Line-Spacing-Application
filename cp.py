import math


class Cp:
    def __init__(self, filename):
        self.lines = []
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        with open(filename, 'r') as cp:

            while True:
                next_line = cp.readline()

                if not next_line:
                    break

                [type, x1, y1, x2, y2] = next_line.split(" ")

                #if x2 < x1:
                 #   x1, y1, x2, y2 = x2, y2, x1, y1

                cp_line = CpLine(int(type), float(x1), float(y1), float(x2), float(y2))


                self.lines.append(cp_line)

                if self.minX > cp_line.x1: self.minX = cp_line.x1
                if self.minX > cp_line.x2: self.minX = cp_line.x2
                if self.minY > cp_line.y1: self.minY = cp_line.y1
                if self.minY > cp_line.y2: self.minY = cp_line.y2

                if self.maxX < cp_line.x1: self.maxX = cp_line.x1
                if self.maxX < cp_line.x2: self.maxX = cp_line.x2
                if self.maxY < cp_line.y1: self.maxY = cp_line.y1
                if self.maxY < cp_line.y2: self.maxY = cp_line.y2

    def size(self):
        width = math.ceil(self.maxX-self.minX)
        height = math.ceil(self.maxY-self.minY)

        return width, height


class CpLine:
    def __init__(self, type: int, x1: float, y1: float, x2: float, y2: float) -> None:
        self.type = type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def color(self):
        if self.type == 1:
            return 0, 0, 0
        if self.type == 2:
            return 255, 0, 0
        if self.type == 3:
            return 0, 0, 255
        if self.type == 4:
            return 193, 193, 193

        raise ValueError("Unknown line type in .cp file")
