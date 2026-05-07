from mazegen import MazeGenerator
from visualizer import MazeRenderer
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
        config.output_file,
        config.perfect,
        config.seed
    )
    maze = mazeGen.generate_maze()
    renderer = MazeRenderer()

    def draw_commands_window(start_y, term_w):
        """
        Fenêtre des commandes affichée sous le maze
        """

        win_h = 8
        win_w = 60

        start_x = max(0, (term_w - win_w) // 2)

        cmd_win = curses.newwin(win_h, win_w, start_y, start_x)

        cmd_win.box()

        cmd_win.addstr(1, 2, "Generate a new maze : Press (R)")
        cmd_win.addstr(2, 2, "Display/Hide the solver : Press (P)")
        cmd_win.addstr(3, 2, "Change wall colors : Press (C)")
        cmd_win.addstr(4, 2, "Exit : Press (Q)")

        cmd_win.refresh()

        return cmd_win

    def draw_scene(show_path=True):
        stdscr.erase()

        current_h, current_w = stdscr.getmaxyx()
        maze_h = (config.height * 2) + 1
        maze_w = (config.width * 3) + 1
        command_h = 8
        total_h = maze_h + command_h + 2

        if current_h < total_h or current_w < maze_w:
            try:
                stdscr.addstr(0, 0, "Terminal too small!", curses.A_REVERSE)
                stdscr.addstr(1, 0, f"Required: {total_h}x{maze_w}")
                stdscr.addstr(2, 0, f"Current : {current_h}x{current_w}")
            except curses.error:
                pass
            return
        start_y = 1
        start_x = (current_w - maze_w) // 2
        renderer.print_maze(
            stdscr,
            maze,
            config.height,
            config.width,
            start_y,
            start_x
        )

        renderer.print_forty_two(
            stdscr,
            maze,
            config.height,
            config.width,
            start_y,
            start_x
        )

        if show_path:
            renderer.print_way(
                stdscr,
                maze,
                mazeGen.path_visu,
                config.height,
                config.width,
                start_y,
                start_x,
                config.entry,
                config.exit
            )
        command_y = start_y + maze_h + 1
        draw_commands_window(command_y, current_w)

    show_path = True
    draw_scene(show_path)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_RESIZE:
            draw_scene(show_path)

        elif key in [ord('q'), ord('Q')]:
            break

        elif key in [ord('p'), ord('P')]:
            show_path = not show_path
            draw_scene(show_path)

        elif key in [ord('c'), ord('C')]:
            renderer.change_color()
            draw_scene(show_path)

        elif key in [ord('r'), ord('R')]:

            mazeGen = MazeGenerator(
                config.height,
                config.width,
                config.entry,
                config.exit,
                config.output_file,
                config.perfect,
                config.seed
            )

            maze = mazeGen.generate_maze()

            draw_scene(show_path)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print("ERROR ERROR ERROR:", e)