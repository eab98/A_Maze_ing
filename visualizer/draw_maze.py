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
        curses.start_color() 
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_CYAN)
        
        WALL_STYLE = curses.color_pair(1) | curses.A_BOLD

        try:
            stdsrc.attron(WALL_STYLE)
            for y in range(height):
                for x in range(width):
                    char = "+--" if maze[y][x].north == 1 else "+  "
                    stdsrc.addstr(char)
                stdsrc.addstr("+")
                
                stdsrc.move(stdsrc.getyx()[0] + 1, 0)

                for x in range(width):
                    wall_char = "|  " if maze[y][x].west == 1 else "   "
                    stdsrc.addstr(wall_char)
                
                if maze[y][width-1].east == 1:
                    stdsrc.addstr("|")

                stdsrc.move(stdsrc.getyx()[0] + 1, 0)

            for x in range(width):
                char = "+--" if maze[height-1][x].south == 1 else "+  "
                stdsrc.addstr(char)
            stdsrc.addstr("+")
            stdsrc.attroff(WALL_STYLE)
            
        except curses.error:
            pass
        stdsrc.refresh()


    def color_eande(self, stdsrc, entry_coords, exit_coords, maze_height, maze_width):
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        
        ex, ey = entry_coords
        xx, xy = exit_coords

        ey = max(0, min(ey, maze_height - 1))
        ex = max(0, min(ex, maze_width - 1))
        xy = max(0, min(xy, maze_height - 1))
        xx = max(0, min(xx, maze_width - 1))

        try:
            stdsrc.attron(curses.color_pair(2))
            stdsrc.addstr(ey * 2 + 1, ex * 3 + 1, "EN")
            stdsrc.attroff(curses.color_pair(2))

            stdsrc.attron(curses.color_pair(3))
            stdsrc.addstr(xy * 2 + 1, xx * 3 + 1, "EX")
            stdsrc.attroff(curses.color_pair(3))
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

    def render_centered_maze(self, stdscr, maze, height, width):
        # 1. Get terminal dimensions
        screen_h, screen_w = stdscr.getmaxyx()

        # 2. Calculate maze dimensions in characters
        # Each cell is 2 lines high and 3 chars wide (+ the final borders)
        maze_render_h = height * 2 + 1
        maze_render_w = width * 3 + 1

        # 3. Calculate start positions to center it
        start_y = (screen_h - maze_render_h) // 2
        start_x = (screen_w - maze_render_w) // 2

        # 4. Create the maze window
        # Params: (height, width, start_y, start_x)
        if screen_h > maze_render_h and screen_w > maze_render_w:
            maze_win = curses.newwin(maze_render_h, maze_render_w, start_y, start_x)
            # Draw the maze inside this window
            self.print_maze(maze_win, maze, height, width)
            return maze_win
        else:
            stdscr.addstr(0, 0, "Terminal too small to center maze!")
            stdscr.refresh()
            return None

    def create_info_window(self, stdscr):
        screen_h, screen_w = stdscr.getmaxyx()
        # Create a window at the bottom of the screen
        info_win = curses.newwin(3, screen_w, screen_h - 3, 0)
        info_win.box() # Draws a border around the interaction window
        info_win.addstr(1, 2, "Use WASD to move | Press 'Q' to Quit")
        info_win.refresh()
        return info_win
    

