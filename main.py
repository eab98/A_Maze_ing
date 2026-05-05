from mazegen import Cell
import curses

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
    height = 5
    width = 5

    maze = create_maze(height, width)
    y, x = 2, 2
    if x + 1 < width:
        maze[y][x].east = 0
        maze[y][x + 1].west = 0

    if y + 1 < height:
        maze[y][x].south = 0
        maze[y + 1][x].north = 0
 
print_maze(maze, height, width)

