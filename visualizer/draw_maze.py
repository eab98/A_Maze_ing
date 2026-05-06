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


    def shared_north(self, maze, x, y):
        if y > 0 and maze[y][x - 1].south == 1:
            return True
        return False


    def shared_west(self, maze,  x, y):
        if x > 0 and maze[y - 1][x].east == 1:
            return True
        return False


    def print_maze(self, stdsrc, maze, height, width):
        stdsrc.clear()
        try:
            for y in range(height):
                for x in range(width):
                    stdsrc.addstr("+--" if maze[y][x].north == 1 else "+  ")
                stdsrc.addstr("+")
                curr_y, _ = stdsrc.getyx()
                stdsrc.move(curr_y + 1, 0)

                for x in range(width):
                    stdsrc.addstr("|  " if maze[y][x].west == 1 else "   ")
                    
                if maze[y][width-1].east == 1:
                    stdsrc.addstr("|")

                curr_y, _ = stdsrc.getyx()
                stdsrc.move(curr_y + 1, 0)

            for x in range(width):
                stdsrc.addstr("+--" if maze[height-1][x].south == 1 else "+  ")
            stdsrc.addstr("+")
        except curses.error:
            pass
        stdsrc.refresh()


    def loading_animation(self, duration=20):
        for i in range(duration + 1):
            percent = (i / duration) * 100
            bar = '█' * i + '-' * (duration - i)
            sys.stdout.write(f'\rRécupération des données : |{bar}| {percent:.0f}%')
            sys.stdout.flush()
            time.sleep(0.1)
        print("\nTerminé ! 🎉")


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
    
	
    def color_eande(self, stdsrc, entry_coords, exit_coords, maze_height, maze_width):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        entry_y, entry_x = entry_coords
        exit_y, exit_x = exit_coords
        try:
            stdsrc.attron(curses.color_pair(1))
            stdsrc.addstr(entry_y * 2 + 1, entry_x * 3 + 1, "EN")
            stdsrc.attroff(curses.color_pair(1))

            stdsrc.attron(curses.color_pair(2))
            stdsrc.addstr(exit_y * 2 + 1, exit_x * 3 + 1, "EX")
            stdsrc.attroff(curses.color_pair(2))
        except curses.error:
            pass
        stdsrc.refresh()

