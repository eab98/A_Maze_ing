from mazegen import MazeGenerator, EntryExitFortyTwoError
from visualizer import MazeRenderer
from parsing import load_config
import curses


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.bkgd(' ', curses.color_pair(0))
    config = load_config("config.txt")

    mazeGen = MazeGenerator(
        config.height, config.width, config.entry, config.exit,
        config.output_file, config.perfect, config.seed
    )
    maze = mazeGen.generate_starting_maze()
    forty_two = True
    try:
        mazeGen.set_forty_two(maze)
    except ValueError as e:
        forty_two = False
    maze = mazeGen.generate_maze(maze)
    renderer = MazeRenderer()

    show_path = True
    path_already_animated = False

    def draw_scene(show_path=True, force_animate=False):
        nonlocal path_already_animated

        stdscr.clear()
        stdscr.refresh()

        current_h, current_w = stdscr.getmaxyx()
        maze_h = (config.height * 2) + 1
        maze_w = (config.width * 3) + 1
        margin_top = 5
        total_h = maze_h + 8 + margin_top + 2

        if current_h < total_h or current_w < maze_w:
            stdscr.addstr(0, 0, "Terminal trop petit !")
            stdscr.refresh()
            return

        title_win = curses.newwin(3, current_w, 1, 0)
        title = "=== A-MAZE-ING GENERATOR ==="
        t_x = max(0, (current_w - len(title)) // 2)
        title_win.attron(curses.A_BOLD | curses.A_UNDERLINE)
        title_win.addstr(1, t_x, title)
        title_win.refresh()

        start_x = (current_w - maze_w) // 2
        maze_win = curses.newwin(maze_h + 1, maze_w + 1, margin_top, start_x)

        renderer.print_maze(maze_win, maze, config.height, config.width, 0, 0)
        renderer.print_forty_two(maze_win,
                                 maze,
                                 config.height,
                                 config.width, 0, 0)

        if show_path:
            should_animate = force_animate and not path_already_animated

            renderer.print_way(
                maze_win, maze, mazeGen.path_visu, config.height, config.width,
                0, 0, config.entry, config.exit,
                animate=should_animate
            )

            if should_animate:
                path_already_animated = True

        maze_win.refresh()

        cmd_h, cmd_w = 8, 60
        cmd_y = margin_top + maze_h + 1
        cmd_x = max(0, (current_w - cmd_w) // 2)
        cmd_win = curses.newwin(cmd_h, cmd_w, cmd_y, cmd_x)
        cmd_win.box()
        cmd_win.addstr(1, 2, "Generate a new maze : Press (R)")
        cmd_win.addstr(2, 2, "Display/Hide the path : Press (P)")
        cmd_win.addstr(3, 2, "Change wall colors : Press (C)")
        cmd_win.addstr(4, 2, "Exit : Press (Q)")
        if not forty_two:
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            ALERT_COLOR = curses.color_pair(1)
            cmd_win.attron(ALERT_COLOR)
            cmd_win.addstr(6, 2, "Maze is too small to display 42")
            cmd_win.attroff(ALERT_COLOR)
        cmd_win.refresh()

    draw_scene(show_path, force_animate=True)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            draw_scene(show_path, force_animate=False)

        elif key in [ord('q'), ord('Q')]:
            break

        elif key in [ord('p'), ord('P')]:
            show_path = not show_path
            draw_scene(show_path, force_animate=True)

        elif key in [ord('c'), ord('C')]:
            renderer.change_color()
            draw_scene(show_path, force_animate=False)

        elif key in [ord('r'), ord('R')]:
            path_already_animated = False
            mazeGen = MazeGenerator(
                config.height, config.width, config.entry, config.exit,
                config.output_file, config.perfect, config.seed
            )
            maze = mazeGen.generate_starting_maze()
            forty_two = True
            try:
                mazeGen.set_forty_two(maze)
            except ValueError as e:
                forty_two = False
            maze = mazeGen.generate_maze(maze)
            renderer = MazeRenderer()
            draw_scene(show_path, force_animate=True)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print("On a vu tkt:\n", e)
