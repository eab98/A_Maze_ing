import curses

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()


    height, width = 12, 60
    start_y, start_x = 3, 3


    win = curses.newwin(height, width, start_y, start_x)
    win.box()

    text = ""
    y, x = 5, 5

    win.addstr(1, 2, "Generate a new maze : Press (R)")
    win.addstr(2, 2, "Display/Hide the solver : Press (P)")
    win.addstr(3, 2, "Change the colors of the wall : Press (C)")
    win.addstr(4, 2, "Exit : Press (Q)")

    while True:
        win.move(y, x)
        win.addstr(y, x, "You chose: " + text)
        win.refresh()
        key = win.getch()
        if key == ord("q"):
            break

        elif key == curses.KEY_LEFT:
            x = max(1, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(width - 20, x + 1)
        elif key == curses.KEY_UP:
            y = max(1, y - 1)
        elif key == curses.KEY_DOWN:
            y = min(height - 2, y + 1)

        elif key in (127, curses.KEY_BACKSPACE):
            text = text[:-1]

        elif 32 <= key <= 126:
            text += chr(key)

    win.getch()


if __name__ == "__main__":
    curses.wrapper(main)