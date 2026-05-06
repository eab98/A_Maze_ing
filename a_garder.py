# animation texte :

import sys
import time

def typewriter(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush() # Force l'affichage du caractère
        time.sleep(delay)
    print() # Retour à la ligne à la fin
    

# cadre pour ecrire :

import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    curses.curs_set(1)

    stdscr.addstr(0, 0, "Enter message (Entrée pour valider)")

    editwin = curses.newwin(5, 30, 2, 1)
    rectangle(stdscr, 1, 0, 7, 32)
    stdscr.refresh()

    box = Textbox(editwin)

    # fonction pour intercepter les touches
    def validate(ch):
        if ch == 10:  # touche Entrée
            return 7  # simule Ctrl-G → termine l'édition
        return ch

    box.edit(validate)

    message = box.gather()

    stdscr.addstr(10, 0, "Message:")
    stdscr.addstr(11, 0, message)

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)

# bouger le texte : 

import curses

def main(stdscr):
    stdscr.keypad(True)
    y, x = 5, 5
    label = "Move me!"
    while True:
        stdscr.clear()
        stdscr.addstr(y, x, label)
        stdscr.refresh()
        key = stdscr.getch()
        rows, cols = stdscr.getmaxyx()
        if key == curses.KEY_UP:
            y = max(0, y - 1)
        elif key == curses.KEY_DOWN:
            y = min(rows - 1, y + 1)
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(cols - len(label) - 1, x + 1)
        elif key == ord("q"):
            break

curses.wrapper(main)