from mazegen import Cell
import curses
import time
import random
from typing import Any


class MazeRenderer:
    def __init__(self) -> None:
        """
        Initialize the maze renderer and configure curses color pairs.

        This is where I define the color pairs used in the functions.
        Values from 1 to 6 correspond to wall colors,
        which will be selected randomly.
        Values from 10 to 12 correspond to the entrance and exit colors,
        and 42 represents the center of the maze.
        """
        curses.start_color()
        self.wall_colors = [1, 2, 3, 4, 5, 6]

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.wall_color = curses.color_pair(random.choice(self.wall_colors))
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(12, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)

    def create_maze(self, height: int, width: int) -> list[list[Cell]]:
        """
        Create a 2D grid of Cell objects representing the maze.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.

        Returns:
            A two-dimensional list containing initialized Cell objects.
        """
        maze = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Cell(x, y))
            maze.append(line)
        return maze

    def which_color(self) -> int:
        """
        Return the currently selected wall color.

        Returns:
        The curses color pair currently used for maze walls.
        """
        return self.wall_color

    def change_color(self) -> None:
        """
        Randomly select and apply a new wall color.

        The new color is chosen from the predefined list of wall colors.
        """
        self.wall_color = curses.color_pair(random.choice(self.wall_colors))

    def print_maze(self, stdsrc: Any, maze: list[list[Cell]], height: int,
                   width: int, start_y: Any, start_x: Any) -> None:
        """
        Render the maze structure on the terminal window.

        The function draws all maze walls using ASCII characters and
        applies the currently selected wall color.

        Args:
            stdsrc: The curses window where the maze is displayed.
            maze: The 2D list of Cell objects representing the maze.
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            start_y: Vertical offset where rendering begins.
            start_x: Horizontal offset where rendering begins.
        """
        stdsrc.clear()
        WALL_COLOR = self.which_color()
        try:
            stdsrc.attron(WALL_COLOR)
            for y in range(height):
                stdsrc.move(start_y + (y * 2), start_x)
                for x in range(width):
                    char = "+--" if maze[y][x].north == 1 else "+  "
                    stdsrc.addstr(char)
                stdsrc.addstr("+")

                stdsrc.move(start_y + (y * 2) + 1, start_x)

                for x in range(width):
                    wall_char = "|  " if maze[y][x].west == 1 else "   "
                    stdsrc.addstr(wall_char)

                if maze[y][width-1].east == 1:
                    stdsrc.addstr("|")

                stdsrc.move(start_y + (height * 2), start_x)

            for x in range(width):
                char = "+--" if maze[height-1][x].south == 1 else "+  "
                stdsrc.addstr(char)
            stdsrc.addstr("+")
            stdsrc.attroff(WALL_COLOR)

        except curses.error:
            pass
        stdsrc.refresh()

    def print_way(self, stdsrc: Any, maze: list[list[Cell]], path: list[Cell],
                  height: int, width: int,
                  start_y: Any, start_x: Any, entry: Any,
                  exit: Any, animate: bool = False) -> None:
        """
        Render the solution path inside the maze.

        The path is displayed with a dedicated color and can optionally
        be animated step by step. Entry and exit cells are highlighted
        with labels.

        Args:
            stdsrc: The curses window where the path is displayed.
            maze: The 2D list of Cell objects representing the maze.
            path: List of cells forming the solution path.
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            start_y: Vertical offset where rendering begins.
            start_x: Horizontal offset where rendering begins.
            entry: Coordinates of the maze entry point.
            exit: Coordinates of the maze exit point.
            animate: If True, displays the path progressively.
        """

        WAY_COLOR = curses.color_pair(11)
        try:
            stdsrc.attron(WAY_COLOR)
            for cell in path:
                x, y = cell.coords
                pos_y = start_y + (y * 2) + 1
                pos_x = start_x + (x * 3) + 1

                stdsrc.addstr(pos_y, pos_x, "  ")

                if x < width - 1 and cell.east == 0 and maze[y][x+1].on_path:
                    stdsrc.addstr(pos_y, pos_x + 2, " ")

                if y < height - 1 and cell.south == 0 and maze[y+1][x].on_path:
                    stdsrc.addstr(pos_y + 1, pos_x, "  ")

                if animate:
                    stdsrc.refresh()
                    time.sleep(0.025)

                if (x, y) == entry:
                    ex, ey = entry
                    stdsrc.attron(curses.color_pair(10) | curses.A_BOLD)
                    stdsrc.addstr(start_y + (ey * 2) + 1,
                                  start_x + (ex * 3) + 1, "EN")
                    stdsrc.attroff(curses.color_pair(10) | curses.A_BOLD)
                    stdsrc.attron(WAY_COLOR)

                if (x, y) == exit:
                    xx, xy = exit
                    stdsrc.attron(curses.color_pair(10) | curses.A_BOLD)
                    stdsrc.addstr(start_y + (xy * 2) + 1,
                                  start_x + (xx * 3) + 1, "EX")
                    stdsrc.attroff(curses.color_pair(10) | curses.A_BOLD)
                    stdsrc.attron(WAY_COLOR)

            stdsrc.attroff(WAY_COLOR)
        except curses.error:
            pass
        stdsrc.refresh()

    def print_forty_two(self, stdsrc: Any, maze: list[list[Cell]],
                        height: int, width: int, start_y: Any,
                        start_x: Any) -> None:
        """
        Highlight cells marked with the `forty_two` attribute.

        Connected highlighted cells are visually linked when no wall
        separates them.

        Args:
            stdsrc: The curses window where the highlighted
            cells are displayed.
            maze: The 2D list of Cell objects representing the maze.
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            start_y: Vertical offset where rendering begins.
            start_x: Horizontal offset where rendering begins.
        """
        WAY_COLOR = curses.color_pair(12)
        try:
            stdsrc.attron(WAY_COLOR)
            for y in range(height):
                for x in range(width):
                    cell = maze[y][x]
                    if cell.forty_two:
                        pos_y = start_y + (y * 2) + 1
                        pos_x = start_x + (x * 3) + 1

                        stdsrc.addstr(pos_y, pos_x, "  ")

                        if (x < width - 1 and cell.east == 0
                                and maze[y][x+1].forty_two):
                            stdsrc.addstr(pos_y, pos_x + 2, " ")

                        if (y < height - 1 and cell.south == 0
                                and maze[y+1][x].forty_two):
                            stdsrc.addstr(pos_y + 1, pos_x, "  ")
            stdsrc.attroff(WAY_COLOR)
        except curses.error:
            pass
        stdsrc.refresh()
