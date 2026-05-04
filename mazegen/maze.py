class Cell:
    def __init__(self, n, s, e, w):
        self.north = n
        self.south = s
        self.east = e
        self.west = w
        self.visited = False

    def is_visited(self) -> bool:
        return self.visited

    def visit(self) -> None:
        self.visited = True


class MazeGenerator:
    def __init__(self, height: int, width: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: int) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

    def generate_starting_maze(self) -> list[list[Cell]]:
        """
        Generates a starting maze filled with fully enclosed cells
        :return: A list of lists representing the starting maze where each list represents a line
        """
        maze = []
        for y in range(self.height):
            maze.append([])
            for x in range(self.width):
                maze[y].append(Cell(1, 1, 1, 1))
        return maze
    
    def generate_maze(self) -> list[list[Cell]]:
       maze = self.generate_starting_maze()
       return maze
