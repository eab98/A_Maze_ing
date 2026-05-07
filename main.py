from mazegen import MazeGenerator
from visualizer import MazeRenderer
import curses
from parsing import load_config


def main(stdscr):
    #Efface le curseur
    curses.curs_set(0)
    #Generation du maze
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
    # Draw the maze
    def draw_scene():
        # Nettoie le terminal
        stdscr.erase()
        # Calcule la taille nécessaire pour afficher tout le maze
        current_h, current_w = stdscr.getmaxyx()
        req_h = (config.height * 2) + 1
        req_w = (config.width * 3) + 1
        if current_h < req_h or current_w < req_w:
            try:
                if current_h > 0:
                    stdscr.addstr(0, 0, "Terminal too small !", curses.A_REVERSE)
                if current_h > 1:
                    stdscr.addstr(1, 0, f"Request: {req_h}x{req_w}")
                if current_h > 2:
                    stdscr.addstr(2, 0, f"Actual: {current_h}x{current_w}")
            except curses.error:
                pass
        #Si tout est bon, dessine le maze
        else:
            start_y = (current_h - req_h) // 2
            start_x = (current_w - req_w) // 2
            try:
                renderer.print_maze(stdscr, maze, config.height, config.width, start_y, start_x)
                renderer.print_forty_two(stdscr, maze, config.height, config.width, start_y, start_x)
                renderer.print_way(stdscr, maze, mazeGen.path_visu, config.height, config.width, start_y, start_x, config.entry, config.exit)
            except curses.error:
                pass
        #Rend visible tout ce qui etait prepare avant
        stdscr.refresh()
    #Fonctions animations
    # renderer.scanner_line("AMAZING")
    # renderer.loading_animation()
    draw_scene()
    # Pour laisser le maze tant que je n'ai pas appuyé sur q
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            draw_scene()
        elif key == ord('q'):
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print("ERROR ERROR ERROR:", e)

