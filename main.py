from mazegen import MazeGenerator
from visualizer import print_maze
from parsing import load_config


if __name__ == "__main__":
    config = load_config("config.txt")
    mazeGen = MazeGenerator(config.height,
                            config.width,
                            config.entry,
                            config.exit,
                            config.perfect,
                            config.seed)
    maze = mazeGen.generate_maze()
    print_maze(maze, config.height, config.width)
