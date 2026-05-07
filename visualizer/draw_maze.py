from mazegen import Cell
import curses
import time
import sys


class MazeRenderer:
    def __init__(self):
        pass

    def create_maze(self, height, width):
        maze = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Cell(x, y))
            maze.append(line)
        return maze

    def print_maze(self, stdsrc, maze, height, width, start_y, start_x):
        stdsrc.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        WALL_COLOR = curses.color_pair(1) | curses.A_BOLD

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

    def loading_animation(self, duration=20):
        for i in range(duration + 1):
            percent = (i / duration) * 100
            bar = '█' * i + '-' * (duration - i)
            sys.stdout.write(f'\rData recovery : |{bar}| {percent:.0f}%')
            sys.stdout.flush()
            time.sleep(0.1)
        print("\n")

    def scanner_line(self, text, width=20, duration=1):
        start_time = time.time()
        while time.time() - start_time < duration:
            for j in range(width):
                if time.time() - start_time >= duration: break
                path = [' '] * width
                path[j] = "●"
                display = "".join(path)
                sys.stdout.write(f'\r{text} [{display}]')
                sys.stdout.flush()
                time.sleep(0.02)
            for j in range(width-1, -1, -1):
                if time.time() - start_time >= duration: break
                path = [' '] * width
                path[j] = "●"
                display = "".join(path)
                sys.stdout.write(f'\r{text} [{display}]')
                sys.stdout.flush()
                time.sleep(0.02)
        print(f"\n{text} [OK]")

    def print_way(self, stdsrc, maze, path, height, width, start_y, start_x, entry, exit):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
        WAY_COLOR = curses.color_pair(4)
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
                stdsrc.refresh()
                time.sleep(0.05)
                if (x, y) == entry:
                    ex, ey = entry
                    stdsrc.attron(curses.color_pair(2) | curses.A_BOLD)
                    stdsrc.addstr(start_y + (ey * 2) + 1, start_x + (ex * 3) + 1, "A*")
                    stdsrc.attroff(curses.color_pair(2) | curses.A_BOLD)
                    stdsrc.attron(WAY_COLOR)

                if (x, y) == exit:
                    xx, xy = exit
                    stdsrc.attron(curses.color_pair(3) | curses.A_BOLD)
                    stdsrc.addstr(start_y + (xy * 2) + 1, start_x + (xx * 3) + 1, "B*")
                    stdsrc.attroff(curses.color_pair(3) | curses.A_BOLD)
            stdsrc.attroff(WAY_COLOR)
        except curses.error:
            pass
        stdsrc.refresh()

    def print_forty_two(self, stdsrc, maze, height, width, start_y, start_x):
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        WAY_COLOR = curses.color_pair(5)
        try:
            stdsrc.attron(WAY_COLOR)
            for y in range(height):
                for x in range(width):
                    cell = maze[y][x]
                    if cell.forty_two:
                        pos_y = start_y + (y * 2) + 1
                        pos_x = start_x + (x * 3) + 1

                        stdsrc.addstr(pos_y, pos_x, "  ") 

                        if x < width - 1 and cell.east == 0 and maze[y][x+1].forty_two:
                            stdsrc.addstr(pos_y, pos_x + 2, " ")

                        if y < height - 1 and cell.south == 0 and maze[y+1][x].forty_two:
                            stdsrc.addstr(pos_y + 1, pos_x, "  ")
            stdsrc.attroff(WAY_COLOR)
        except curses.error:
            pass
        stdsrc.refresh()
