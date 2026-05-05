from mazegen import MazeGenerator
import curses
from visualizer import print_maze, loading_animation, scanner_line
from parsing import load_config


def main(stdsrc):
    config = load_config("config.txt")
    mazeGen = MazeGenerator(config.height,
                            config.width,
                            config.entry,
                            config.exit,
                            config.perfect,
                            config.seed)
    maze = mazeGen.generate_maze()
    scanner_line("AMAZING")
    loading_animation()
    print_maze(stdsrc, maze, config.height, config.width)
    stdsrc.getch()

if __name__ == "__main__":
    curses.wrapper(main)