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
    # renderer.scanner_line("AMAZING")
    # renderer.loading_animation()

    curses.curs_set(0)  
    stdsrc.keypad(True) 
    stdsrc.timeout(100) 

    def redraw():
        stdsrc.clear()
        renderer.print_maze(stdsrc, maze, config.height, config.width)
        # renderer.color_eande(
        #     stdsrc, 
        #     mazeGen.entry, 
        #     mazeGen.exit, 
        #     mazeGen.height, 
        #     mazeGen.width
        # )
        stdsrc.refresh()
    redraw()
    while True:
        key = stdsrc.getch()
        if key == ord('q'):
            break
        if key == curses.KEY_RESIZE or key != -1:
            if key == curses.KEY_RESIZE:
                curses.update_lines_cols() 
            redraw()

if __name__ == "__main__":
    curses.wrapper(main)
