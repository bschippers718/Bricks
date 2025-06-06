#!/usr/bin/env python3
"""Terminal-based Brickles game.

This version of Brickles uses the ``curses`` module so it can run directly
in a terminal window. The bricks are arranged to spell ``HAPPY BIRTHDAY WYATT``
and the player controls a paddle with the left and right arrow keys. When all
bricks are cleared a celebratory message is shown.
"""

import curses
import time
from typing import Dict, List, Tuple

# Define simple 4x5 block letters for required characters
LETTER_PATTERNS: Dict[str, List[str]] = {
    "A": [
        " ## ",
        "#  #",
        "####",
        "#  #",
        "#  #",
    ],
    "B": [
        "### ",
        "#  #",
        "### ",
        "#  #",
        "### ",
    ],
    "D": [
        "### ",
        "#  #",
        "#  #",
        "#  #",
        "### ",
    ],
    "H": [
        "#  #",
        "#  #",
        "####",
        "#  #",
        "#  #",
    ],
    "I": [
        "###",
        " # ",
        " # ",
        " # ",
        "###",
    ],
    "P": [
        "### ",
        "#  #",
        "### ",
        "#   ",
        "#   ",
    ],
    "R": [
        "### ",
        "#  #",
        "### ",
        "# # ",
        "#  #",
    ],
    "T": [
        "####",
        " ## ",
        " ## ",
        " ## ",
        " ## ",
    ],
    "W": [
        "#  #",
        "#  #",
        "#  #",
        "# # ",
        "## #",
    ],
    "Y": [
        "#  #",
        " ## ",
        "  # ",
        "  # ",
        "  # ",
    ],
}

# Game characters
BRICK_CHAR = "#"
BALL_CHAR = "O"
PADDLE_CHAR = "="

PADDLE_WIDTH = 7
DELAY = 0.05  # seconds between frames

MESSAGE = "HAPPY BIRTHDAY WYATT"


def build_message_rows(text: str) -> List[str]:
    """Return a list of strings representing the brick layout for ``text``."""
    rows = ["" for _ in range(5)]
    for ch in text.upper():
        if ch == " ":
            for i in range(5):
                rows[i] += "    "  # 4 spaces gap for spaces
            continue
        pattern = LETTER_PATTERNS.get(ch)
        if not pattern:
            continue
        for i in range(5):
            rows[i] += pattern[i] + " "
    return rows


def create_bricks(rows: List[str], limit_x: int, limit_y: int) -> List[Tuple[int, int]]:
    """Return list of (y, x) brick coordinates within the screen limits."""
    bricks = []
    for y, row in enumerate(rows):
        if y >= limit_y:
            break
        for x, ch in enumerate(row):
            if x >= limit_x:
                break
            if ch != " ":
                bricks.append((y, x))
    return bricks


def main(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    max_y, max_x = stdscr.getmaxyx()
    rows = build_message_rows(MESSAGE)
    bricks = create_bricks(rows, max_x, max_y)
    paddle_y = min(len(rows) + 2, max_y - 2)
    paddle_x = max_x // 2 - PADDLE_WIDTH // 2
    ball_y = paddle_y - 1
    ball_x = paddle_x + PADDLE_WIDTH // 2
    dx, dy = 1, -1

    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            paddle_x = max(0, paddle_x - 2)
        elif key == curses.KEY_RIGHT:
            paddle_x = min(max_x - PADDLE_WIDTH, paddle_x + 2)
        elif key == ord("q"):
            break

        next_x = ball_x + dx
        next_y = ball_y + dy

        # Wall collisions
        if next_x <= 0 or next_x >= max_x - 1:
            dx *= -1
            next_x = ball_x + dx
        if next_y <= 0:
            dy *= -1
            next_y = ball_y + dy
        if next_y >= max_y:
            stdscr.nodelay(False)
            stdscr.addstr(max_y // 2, max_x // 2 - 5, "Game Over")
            stdscr.getch()
            break

        # Paddle collision
        if next_y == paddle_y and paddle_x <= next_x < paddle_x + PADDLE_WIDTH:
            dy *= -1
            next_y = ball_y + dy

        # Brick collision
        if (next_y, next_x) in bricks:
            bricks.remove((next_y, next_x))
            dy *= -1
            next_y = ball_y + dy

        ball_x, ball_y = next_x, next_y

        stdscr.clear()
        for y, x in bricks:
            stdscr.addch(y, x, BRICK_CHAR)
        for i in range(PADDLE_WIDTH):
            stdscr.addch(paddle_y, paddle_x + i, PADDLE_CHAR)
        stdscr.addch(ball_y, ball_x, BALL_CHAR)
        stdscr.refresh()

        if not bricks:
            stdscr.nodelay(False)
            msg = "Happy Birthday Wyatt!"
            stdscr.addstr(max_y // 2, max_x // 2 - len(msg) // 2, msg)
            stdscr.getch()
            break

        time.sleep(DELAY)


if __name__ == "__main__":
    curses.wrapper(main)
