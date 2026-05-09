from mazegen import Cell
import curses
import time
import random
from typing import Any


class MazeRenderer:
    def __init__(self) -> None:
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
        maze = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Cell(x, y))
            maze.append(line)
        return maze

    def which_color(self) -> int:
        return self.wall_color

    def change_color(self) -> None:
        self.wall_color = curses.color_pair(random.choice(self.wall_colors))

    def print_maze(self, stdsrc: Any, maze: Any, height: Any,
                   width: Any, start_y: Any, start_x: Any) -> None:
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

    def print_way(self, stdsrc: Any, maze: Any, path: Any,
                  height: Any, width: Any,
                  start_y: Any, start_x: Any, entry: Any,
                  exit: Any, animate: bool = False) -> None:
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

    def print_forty_two(self, stdsrc: Any, maze: Any,
                        height: Any, width: Any, start_y: Any,
                        start_x: Any) -> None:
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
