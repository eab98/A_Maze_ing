from mazegen import Cell
import curses
import time
import sys

def create_maze(height, width):
    maze = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(Cell(x, y)) 
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


def print_maze(stdsrc, maze, height, width):
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

def loading_animation(duration=20):
    for i in range(duration + 1):
        percent = (i / duration) * 100
        bar = '█' * i + '-' * (duration - i)
        sys.stdout.write(f'\rRécupération des données : |{bar}| {percent:.0f}%')
        sys.stdout.flush()
        time.sleep(0.1)
    print("\nTerminé ! 🎉")

def scanner_line(text, width=20, duration=5):
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

