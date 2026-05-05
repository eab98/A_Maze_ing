import curses

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.addstr(0, 0, "Just for the test", curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
