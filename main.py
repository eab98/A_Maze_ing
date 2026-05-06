from mazegen import MazeGenerator
from visualizer import MazeRenderer
import curses
from parsing import load_config


import curses

def main(stdscr):
    curses.curs_set(0)

    config = load_config("config.txt")
    mazeGen = MazeGenerator(
        config.height,
        config.width,
        config.entry,
        config.exit,
        config.perfect,
        config.seed
    )
    maze = mazeGen.generate_maze()
    renderer = MazeRenderer()

    def draw_scene():
        stdscr.erase()
        current_h, current_w = stdscr.getmaxyx()

        req_h = config.height + 2
        req_w = (config.width * 2) + 2

        if current_h < req_h or current_w < req_w:
            try:
                if current_h > 0:
                    stdscr.addstr(0, 0, "Terminal trop petit !", curses.A_REVERSE)
                if current_h > 1:
                    stdscr.addstr(1, 0, f"Requis: {req_h}x{req_w}")
                if current_h > 2:
                    stdscr.addstr(2, 0, f"Actuel: {current_h}x{current_w}")
            except curses.error:
                pass
        else:
            try:
                renderer.print_maze(stdscr, maze, config.height, config.width)
                renderer.color_eande(
                    stdscr,
                    mazeGen.entry,
                    mazeGen.exit,
                    mazeGen.height,
                    mazeGen.width
                )
            except curses.error:
                pass

        stdscr.refresh()

    draw_scene()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            draw_scene()

        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

