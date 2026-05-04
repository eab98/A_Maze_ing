class Cell:
    def __init__(self, north: int, south: int, east: int, west: int) -> None:
        self.__north = north
        self.__south = south
        self.__east = east
        self.__west = west
        self.__visited = False

    def get_north(self) -> int:
        return self.__north

    def set_north(self, state: int) -> None:
        self.__north = state

    def get_south(self) -> int:
        return self.__south

    def set_south(self, state: int) -> None:
        self.__south = state

    def get_east(self) -> int:
        return self.__east

    def set_east(self, state: int) -> None:
        self.__east = state

    def get_west(self) -> int:
        return self.__west

    def set_west(self, state: int) -> None:
        self.__west = state

    def is_visited(self) -> bool:
        return self.__visited

    def visit(self) -> None:
        self.__visited = True


def first_line(width: int):
    line = []
    for i in range(width):
        if i == 0:
            cellule = Cell(1, 0, 0, 1)
        elif i == width - 1:
            cellule = Cell(1, 0, 1, 0)
        else:
            cellule = Cell(1, 0, 0, 0)
        line.append(cellule)
    return line


def middle_line(width: int):
    line = []
    for i in range(width):
        if i == 0:
            cellule = Cell(0, 0, 0, 1)
        elif i == width - 1:
            cellule = Cell(0, 0, 1, 0)
        else:
            cellule = Cell(0, 0, 0, 0)
        line.append(cellule)
    return line


def last_line(width: int):
    line = []
    for i in range(width):
        if i == 0:
            cellule = Cell(0, 1, 0, 1)
        elif i == width - 1:
            cellule = Cell(0, 1, 1, 0)
        else:
            cellule = Cell(0, 1, 0, 0)
        line.append(cellule)
    return line


def generate_maze(height: int, width: int):
    maze = []
    for i in range(height):
        line = []
        if i == 0:
            line = first_line(width)
        elif i == height - 1:
            line = last_line(width)
        else:
            line = middle_line(width)
        maze.append(line)
    return maze


def print_maze(maze):
    for line in maze:
        for cell in line:
            print(end="+ ")
            if cell.get_north() == 1:
                print("- ", end="")
            else:
                print("  ", end="")
        print("+", end="")
        print()

        for cell in line:
            if cell.get_west() == 1:
                print("|", end="")
            else:
                print(" ", end="")
            print("  ", end="")

            if cell.get_east() == 1:
                print("|", end="")
            else:
                print(" ", end="")
        print()

        for cell in line:
            print("+ ", end="")
            if cell.get_south() == 1:
                print("- ", end="")
            else:
                print("  ", end="")
        print("+", end="")
        print()


if __name__ == "__main__":
    maze = generate_maze(15, 15)
    print_maze(maze)
