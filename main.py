from mazegen import Cell


def create_maze(height, width):
    maze = []
    for i in range(height):
        line = []
        for i in range(width):
            line.append(Cell(1, 1, 1, 1))
        maze.append(line)
    return maze


def shared_north(maze, width, height, x, y):
    if y > 0 and maze[y][x - 1].south == 1:
        return True
    return False


def shared_west(maze, width, height, x, y):
    if x > 0 and maze[y - 1][x].east == 1:
        return True
    return False


def print_maze(maze, height, width):
    for y in range(height):
        for x in range(width):
            if maze[y][x].north == 1 and not shared_north(maze, width,
                                                          height, x, y):
                if x < width - 1:
                    print(" ---", end="")
                else:
                    print(" ---")
        for x in range(width):
            if maze[y][x].west == 1 and not shared_west(maze, width,
                                                        height, x, y):
                print("|", end="")

        for x in range(width):
            if maze[y][x].east == 1:
                if x < width - 1:
                    print("   |", end="")
                else:
                    print("   |")
        for x in range(width):
            if maze[y][x].south == 1:
                if x < width - 1:
                    print(" ---", end="")
                else:
                    print(" ---")


if __name__ == "__main__":
    maze = create_maze(10, 10)
    print_maze(maze, 10, 10)
