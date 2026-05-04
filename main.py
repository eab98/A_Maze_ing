class Cell:
    def __init__(self, n, s, e, w):
        self.north = n
        self.south = s
        self.east = e
        self.west = w
        self.visited = False

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


def create_maze(height, width):
    maze = []
    for i in range(height):
        line = []
        for i in range(width):
            line.append(Cell(1, 1, 1, 1))
        maze.append(line)
    return maze


def shared_north(maze, x, y):
    if y > 0 and maze[y][x - 1].south == 1:
        return True
    return False


def shared_west(maze,  x, y):
    if x > 0 and maze[y - 1][x].east == 1:
        return True
    return False


def print_maze(maze, height, width):
    for y in range(height):
        for x in range(width):
            if maze[y][x].north == 1:
                print("+--", end="")
            else:
                print("+  ", end="")
        print("+")

        for x in range(width):
            if maze[y][x].west == 1:
                print("|  ", end="")
            else:
                print("   ", end="")
        if maze[y][width-1].east == 1:
            print("|")
        else:
            print(" ")
            
    for x in range(width):
        if maze[height-1][x].south == 1:
            print("+--", end="")
        else:
            print("+  ", end="")
    print("+")


if __name__ == "__main__":
    height = 10
    width = 10
    maze = create_maze(height, width)
    y, x = 5, 3
    if x + 1 < width:
        maze[y][x].east = 0
        maze[y][x+1].west = 0
    if y + 1 < height:
        maze[y][x].south = 0
        maze[y+1][x].north = 0
    print_maze(maze, height, width)
