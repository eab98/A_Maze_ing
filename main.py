from mazegen import MazeGenerator
from visualizer import MazeRenderer
import curses
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
    renderer = MazeRenderer()
    renderer.scanner_line("AMAZING")
    renderer.loading_animation()
    renderer.print_maze(stdsrc, maze, config.height, config.width)
    renderer.color_eande(
        stdsrc, 
        mazeGen.entry, 
        mazeGen.exit, 
        mazeGen.height, 
        mazeGen.width
    )
    print(mazeGen.path)
    stdsrc.getch()

if __name__ == "__main__":
    curses.wrapper(main)