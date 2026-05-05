from mazegen import MazeGenerator



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
    mazeGen = MazeGenerator(10, 15,(0,0), (15,15), True)
    maze = mazeGen.generate_maze()
    print_maze(maze, mazeGen.height, mazeGen.width)