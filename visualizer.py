def print_maze(maze, height, width):
    for y in range(height):
        for x in range(width):
            if maze[y][x].north == 1 and not shared_north(maze, x, y):
                if x < width - 1:
                    print("+--", end="")
                else:
                    print("+--+")
        for x in range(width):
            if maze[y][x].west == 1 and not shared_west(maze, x, y):
                print("|", end="")

        for x in range(width):
            if maze[y][x].east == 1:
                if x < width - 1:
                    print("  |", end="")
                else:
                    print("  |")
        for x in range(width):
            if maze[y][x].south == 1:
                if x < width - 1:
                    print("+--", end="")
                else:
                    print("+--+")