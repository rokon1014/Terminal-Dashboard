"""
TODO: Add description
"""


from dataclasses import dataclass, field
from typing import List
import curses


@dataclass
class PrintBlock:
    string_with_attrib: List = field(default_factory=lambda: ["what to print", 0])
    block_number: int = 1
    starting_location_row: int = 0
    starting_location_column: int = 0
    title = str


def assigning_attrib(var):
    if var:
        return TerminalDashboard.NOMINAL
    else:
        return TerminalDashboard.DANGER | curses.A_BOLD


class TerminalDashboard:
    def __init__(self):
        # screens and windows
        self.screen = curses.initscr()
        self.num_rows, self.num_cols = self.screen.getmaxyx()
        self.windows = None
        self.current_line = 1
        self.current_row = 1
        self.start_vertical_row = 1

        # Colors
        curses.start_color()

        ## TODO: Add automatic color pairs
        # curses.use_default_colors()
        # if curses.has_colors():
        #     for i in range(0, curses.COLORS):
        #         curses.init_pair(i + 1, i, -1)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)

        TerminalDashboard.DANGER = curses.color_pair(1) | curses.A_BOLD
        TerminalDashboard.NOMINAL = curses.color_pair(2)
        TerminalDashboard.WATCHOUT = curses.color_pair(3)
        TerminalDashboard.MAGENTA = curses.color_pair(4)
        TerminalDashboard.BLUE = curses.color_pair(5)
        TerminalDashboard.CYAN = curses.color_pair(6)
        TerminalDashboard.YELLOW = curses.color_pair(7)
        TerminalDashboard.BAR_YELLOW = curses.color_pair(8)
        TerminalDashboard.BAR_WHITE = curses.color_pair(9)

        # cursor
        curses.curs_set(0)

    def cleanup(self):
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()
        # raise

    def all_refresh(self):
        if self.windows:
            for window in self.windows:
                window.refresh()

        else:
            self.screen.refresh()

    def all_erase(self):
        if self.windows:
            for window in self.windows:
                window.erase()

        else:
            self.screen.erase()

    def run(self):
        try:
            for i in range(0, 255):
                self.screen.addstr(str(i), curses.color_pair(i))

            self.screen.attron(curses.A_BOLD)
            self.screen.bkgd(curses.A_ITALIC)
            self.screen.border()
            self.screen.box()

        except:
            print(curses.error)
            self.cleanup()
            raise

        self.screen.getch()

    def print_info(self, blocks, col):
        try:
            # checking max num of line and columns
            # checking for resize
            self.num_rows, self.num_cols = self.screen.getmaxyx()

            self.current_line = 1

            if col > 1:
                self.current_row = int(self.num_cols / col)
            else:
                self.current_row = 1

            # iterate through each block
            for block in blocks:
                # Empty line at the start of each block
                self.current_line += 1

                # Iterate through each string in current block
                for k, string_to_print in enumerate(block.string_with_attrib):
                    # check for resize
                    if (
                        self.current_line < self.num_rows
                        and len(string_to_print[0]) < self.num_cols
                    ):
                        # First string is always the title
                        if k == 1:
                            attrib = string_to_print[1] | curses.A_BOLD
                        else:
                            attrib = string_to_print[1]

                        # finally printing the string
                        self.screen.addstr(
                            self.current_line,
                            self.current_row,
                            f"{string_to_print[0]}",
                            attrib,
                        )

                        # go to the next line
                        self.current_line += 1

            self.screen.border()
            self.screen.box()

            # self.all_refresh()
            # self.all_erase()

        except Exception as e:
            print(curses.error, e)
            self.cleanup()

    def draw_bar(self, title="title", value=0.0, color=curses.A_BOLD, attrib="normal"):
        try:
            self.num_rows, self.num_cols = self.screen.getmaxyx()

            self.current_line += 2
            full_bar = int(self.num_cols * 0.7)
            current_bar = int(full_bar * value)
            ch = " "

            if attrib is not ("normal" or "blink"):
                raise AssertionError(" DRAW-BAR: Chose attrib between normal or blink")

            if attrib == "normal":
                attrib = curses.A_NORMAL | color
            elif attrib == "blink":
                attrib = curses.A_BLINK | color
            else:
                attrib = curses.A_NORMAL | color

            if (
                self.current_line < self.num_rows
                and (current_bar + len(title) + 3) < self.num_cols
            ):
                self.screen.addstr(
                    self.current_line,
                    1,
                    title,
                )

                self.screen.addstr(
                    self.current_line,
                    len(title) + 1,
                    ch * current_bar,
                    attrib,
                )

                self.screen.addstr(
                    self.current_line,
                    len(title) + current_bar,
                    f"{value:.2f}",
                    color,
                )
                # self.screen.getch()

        except:
            print(curses.error)
            self.cleanup()
            raise

    def draw_vertical_bar(
        self,
        title="title",
        value=0.0,
        color=curses.A_BOLD,
        attrib="normal",
        start_row=40,
    ):
        self.num_rows, self.num_cols = self.screen.getmaxyx()
        self.current_row = start_row
        starting_line = int(self.num_rows / 2)
        try:
            bar_height = starting_line * 0.8
            current_bar = int(bar_height * value)
            ch = " "

            for ii in range(current_bar, 0, -1):
                if (
                    self.current_line < self.num_rows
                    and (starting_line) < self.num_cols
                    and (starting_line - ii) > 2
                    and starting_line - current_bar > 2
                ):
                    self.screen.addstr(starting_line - ii, self.current_row, ch, color)
                    self.screen.addstr(
                        starting_line - ii, self.current_row + 1, ch, color
                    )

                    self.screen.addstr(
                        starting_line - current_bar - 1,
                        self.current_row,
                        f"{value:0.2f}",
                    )
                    self.screen.addstr(
                        starting_line,
                        self.current_row,
                        f"{title}",
                    )

        except:
            print(curses.error)
            self.cleanup()
            raise


if __name__ == "__main__":
    screen_debug = TerminalDashboard()
    screen_debug.run()
    screen_debug.cleanup()
