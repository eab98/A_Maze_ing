from collections import deque
from typing import Deque
import random


class Cell:
    def __init__(self, x: int, y: int):
        self.north = 1
        self.south = 1
        self.east = 1
        self.west = 1
        self.coords = (x, y)
        self.visited = False
        self.on_path = False
        self.forty_two = False

    def is_visited(self) -> bool:
        return self.visited

    def visit(self) -> None:
        self.visited = True

    def get_value(self) -> int:
        return (2**3) * self.west + (2**2) * self.south + 2 * self.east + self.north


class MazeGenerator:
    def __init__(self, height: int, width: int, entry: tuple[int, int],
                 exit: tuple[int, int], output_file: str,
                 perfect: bool,
                 seed: int | None) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = random.Random(seed)
        self.path = []

    def empty_path(self) -> None:
        self.path = []

    def get_direction(self, current: tuple[int, int],
                      next: tuple[int, int]) -> str:
        current_x, current_y = current
        next_x, next_y = next
        if current_x < next_x:
            return 'E'
        elif current_x > next_x:
            return 'W'
        elif current_y < next_y:
            return 'S'
        else:
            return 'N'

    def create_path(self, solution: Deque[Cell]) -> None:
        self.empty_path()
        if solution:
            previous = solution.popleft()
            previous.on_path = True
            self.path.append(self.get_direction(self.entry, previous.coords))
            while solution:
                current = solution.popleft()
                current.on_path = True
                self.path.append(self.get_direction(previous.coords,
                                                    current.coords))
                previous = current
            self.path.append(self.get_direction(previous.coords, self.exit))

    def generate_starting_maze(self) -> list[list[Cell]]:
        """
        Generates a starting maze filled with fully enclosed cells
        :return: A list of lists representing the starting maze where each
        list represents a line
        """
        maze = []
        for y in range(self.height):
            maze.append([])
            for x in range(self.width):
                maze[y].append(Cell(x, y))
        return maze

    def get_neighbour(self, cell: Cell,
                      maze: list[list[Cell]]) -> Cell | None:
        neighbours = []
        cell_x, cell_y = cell.coords
        if cell_x < self.width - 1 and not (maze[cell_y][cell_x + 1].visited or maze[cell_y][cell_x + 1].forty_two):
            neighbours.append(maze[cell_y][cell_x + 1])
        if cell_y < self.height - 1 and not (maze[cell_y + 1][cell_x].visited or maze[cell_y + 1][cell_x].forty_two):
            neighbours.append(maze[cell_y + 1][cell_x])
        if cell_x > 0 and not (maze[cell_y][cell_x - 1].visited or maze[cell_y][cell_x - 1].forty_two):
            neighbours.append(maze[cell_y][cell_x - 1])
        if cell_y > 0 and not (maze[cell_y - 1][cell_x].visited or maze[cell_y - 1][cell_x].forty_two):
            neighbours.append(maze[cell_y - 1][cell_x])
        if len(neighbours) > 0:
            return self.seed.choice(neighbours)
        return None

    def break_wall(self, current: Cell, neighbour: Cell) -> None:
        current_x, current_y = current.coords
        neighbour_x, neighbour_y = neighbour.coords

        if current_x < neighbour_x:
            current.east = 0
            neighbour.west = 0
        elif current_x > neighbour_x:
            current.west = 0
            neighbour.east = 0
        elif current_y < neighbour_y:
            current.south = 0
            neighbour.north = 0
        elif current_y > neighbour_y:
            current.north = 0
            neighbour.south = 0

    def set_four(self, maze: list[list[Cell]], cx: int, cy: int) -> None:
        if self.width % 2 == 0:
            cx -= 1
        maze[cy][cx - 1].forty_two = True
        maze[cy][cx - 2].forty_two = True
        self.break_wall(maze[cy][cx - 1], maze[cy][cx - 2])
        maze[cy][cx - 3].forty_two = True
        self.break_wall(maze[cy][cx - 2], maze[cy][cx - 3])
        maze[cy + 1][cx - 1].forty_two = True
        self.break_wall(maze[cy][cx - 1], maze[cy + 1][cx - 1])
        maze[cy + 2][cx - 1].forty_two = True
        self.break_wall(maze[cy + 2][cx - 1], maze[cy + 1][cx - 1])
        maze[cy - 1][cx - 3].forty_two = True
        self.break_wall(maze[cy][cx - 3], maze[cy - 1][cx - 3])
        maze[cy - 2][cx - 3].forty_two = True
        self.break_wall(maze[cy - 1][cx - 3], maze[cy - 2][cx - 3])

    def set_two(self, maze: list[list[Cell]], cx: int, cy: int) -> None:

        maze[cy][cx + 1].forty_two = True
        maze[cy][cx + 2].forty_two = True
        maze[cy][cx + 3].forty_two = True
        self.break_wall(maze[cy][cx + 1], maze[cy][cx + 2])
        self.break_wall(maze[cy][cx + 3], maze[cy][cx + 2])
        maze[cy - 1][cx + 3].forty_two = True
        maze[cy - 2][cx + 3].forty_two = True
        self.break_wall(maze[cy - 2][cx + 3], maze[cy - 1][cx + 3])
        maze[cy - 2][cx + 2].forty_two = True
        self.break_wall(maze[cy - 2][cx + 2], maze[cy - 2][cx + 3])
        maze[cy - 2][cx + 1].forty_two = True
        self.break_wall(maze[cy - 2][cx + 1], maze[cy - 2][cx + 2])
        maze[cy + 1][cx + 1].forty_two = True
        maze[cy + 2][cx + 1].forty_two = True
        self.break_wall(maze[cy + 1][cx + 1], maze[cy][cx + 1])
        maze[cy + 2][cx + 2].forty_two = True
        self.break_wall(maze[cy + 1][cx + 1], maze[cy + 2][cx + 1])
        self.break_wall(maze[cy + 2][cx + 1], maze[cy + 2][cx + 2])
        maze[cy + 2][cx + 3].forty_two = True
        self.break_wall(maze[cy + 2][cx + 2], maze[cy + 2][cx + 3])
        self.break_wall(maze[cy][cx + 3], maze[cy - 1][cx + 3])



    def set_forty_two(self, maze: list[list[Cell]]) -> None:
        if self.height < 8 or self.width < 10:
            raise ValueError("Maze is too small to display 42")
        center_x = self.width // 2
        center_y = self.height // 2

        self.set_four(maze, center_x, center_y)
        self.set_two(maze, center_x, center_y)

    def generate_output_file(self, maze: list[list[Cell]]) -> None:
        try:
            with open(self.output_file, 'w') as f:
                for line in maze:
                    for cell in line:
                        value = cell.get_value()
                        value_str = f"{value:X}"
                        f.write(value_str)
                    f.write('\n')
                f.write('\n')
                entry_x, entry_y = self.entry
                exit_x, exit_y = self.exit
                f.write(str(entry_x) + ',' + str(entry_y) + '\n')
                f.write(str(exit_x) + ',' + str(exit_y) + '\n')
                for i in self.path:
                    f.write(str(i))
                f.write('\n')

        except FileNotFoundError:
            print("Output file creation impossible")

    def break_random_walls(self, maze: list[list[Cell]], probs: float) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.seed.random() < probs:
                    current = maze[y][x]
                    valid_neighbors = []
                    if x > 0 and current.west == 1 and not current.forty_two:
                        if not maze[y][x - 1].forty_two:
                            valid_neighbors.append(maze[y][x - 1])
                    if x < self.width - 1 and current.east == 1 and not current.forty_two:
                        if not maze[y][x + 1].forty_two:
                            valid_neighbors.append(maze[y][x + 1])
                    if y > 0 and current.north == 1 and not current.forty_two:
                        if not maze[y - 1][x].forty_two:
                            valid_neighbors.append(maze[y - 1][x])
                    if y < self.height - 1 and current.south == 1 and not current.forty_two:
                        if not maze[y + 1][x].forty_two:
                            valid_neighbors.append(maze[y + 1][x])
                    if valid_neighbors:
                        neighbor = self.seed.choice(valid_neighbors)
                        self.break_wall(current, neighbor)

    def get_shortest_path(self, maze: list[list[Cell]]) -> Deque[Cell]:
        start_x, start_y = self.entry

        queue = deque([(maze[start_y][start_x], [maze[start_y][start_x]])])

        visited_coords = {self.entry}
        while queue:
            val = queue.popleft()
            path = val[1]
            current = val[0]
            x, y = current.coords

            if current.coords == self.exit:
                return deque(path[1:-1])

            if current.north == 0 and y > 0 and (x, y - 1) not in visited_coords:
                visited_coords.add((x, y - 1))
                queue.append((maze[y - 1][x], path + [maze[y - 1][x]]))

            if current.south == 0 and y < self.height - 1 and (x, y + 1) not in visited_coords:
                visited_coords.add((x, y + 1))
                queue.append((maze[y + 1][x], path + [maze[y + 1][x]]))

            if current.east == 0 and x < self.width - 1 and (x + 1, y) not in visited_coords:
                visited_coords.add((x + 1, y))
                queue.append((maze[y][x + 1], path + [maze[y][x + 1]]))

            if current.west == 0 and x > 0 and (x - 1, y) not in visited_coords:
                visited_coords.add((x - 1, y))
                queue.append((maze[y][x - 1], path + [maze[y][x - 1]]))

        return deque()



    def generate_maze(self) -> list[list[Cell]]:
        maze = self.generate_starting_maze()
        try:
            self.set_forty_two(maze)
        except ValueError as e:
            print(e)
        start_x, start_y = self.entry
        current = maze[start_y][start_x]
        current.on_path = True
        current.visit()
        visited = deque()
        solution_path = deque()
        path_found: bool = False
        while current is not None:
            neighbour = self.get_neighbour(current, maze)
            if neighbour is not None:
                self.break_wall(current, neighbour)
                neighbour.visit()
                visited.append(current)
                current = neighbour
                if current.coords == self.exit:
                    path_found = True
                    current.on_path = True
                if not path_found:
                    solution_path.append(current)
            elif len(visited) > 0:
                if current.coords == self.exit:
                    path_found = True
                    current.on_path = True
                if not path_found:
                    solution_path.pop()
                current = visited.pop()
            else:
                if not self.perfect:
                    self.break_random_walls(maze, 0.1)
                    solution_path = self.get_shortest_path(maze)
                self.create_path(solution_path)
                self.generate_output_file(maze)
                current = None
        return maze
