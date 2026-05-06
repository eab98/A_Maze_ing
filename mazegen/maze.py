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

    def is_visited(self) -> bool:
        return self.visited

    def visit(self) -> None:
        self.visited = True


class MazeGenerator:
    def __init__(self, height: int, width: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool,
                 seed: int | None) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = random.Random(seed)
        self.path = []

    def empty_path(self) -> None:
        self.path = []

    def get_direction(self, current: tuple[int, int], next: tuple[int, int]) -> str:
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
            self.path.append(self.get_direction(self.entry, previous.coords))
            while solution:
                current = solution.popleft()
                self.path.append(self.get_direction(previous.coords, current.coords))
                previous = current
            self.path.append(self.get_direction(previous.coords, self.exit))


    def generate_starting_maze(self) -> list[list[Cell]]:
        """
        Generates a starting maze filled with fully enclosed cells
        :return: A list of lists representing the starting maze where each list represents a line
        """
        maze = []
        for y in range(self.height):
            maze.append([])
            for x in range(self.width):
                maze[y].append(Cell(x, y))
        return maze

    def get_neighbour(self, cell: Cell, maze: list[list[Cell]]) -> Cell | None:
        neighbours = []
        cell_x, cell_y = cell.coords
        if cell_x < self.width - 1 and not maze[cell_y][cell_x + 1].visited:
           neighbours.append(maze[cell_y][cell_x + 1])
        if cell_y < self.height - 1 and not maze[cell_y + 1][cell_x].visited:
            neighbours.append(maze[cell_y + 1][cell_x])
        if cell_x > 0 and not maze[cell_y][cell_x - 1].visited:
            neighbours.append(maze[cell_y][cell_x - 1])
        if cell_y > 0 and not maze[cell_y - 1][cell_x].visited:
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

    def generate_maze(self) -> list[list[Cell]]:
       maze = self.generate_starting_maze()
       start_x, start_y = self.entry
       current = maze[start_y][start_x]
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
               if not path_found:
                   solution_path.append(current)
           elif len(visited) > 0:
               if current.coords == self.exit:
                   path_found = True
               if not path_found:
                   solution_path.pop()
               current = visited.pop()
           else:
               self.create_path(solution_path)
               current = None
       return maze
