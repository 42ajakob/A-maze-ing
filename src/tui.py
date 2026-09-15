import curses
from typing import Any
from .maze_builder import create_maze
from .parser import MazeConfig
from .maze_io import Maze, parse_output_file
from .render import (
    TAG_WALL, TAG_OPEN, TAG_PATH, TAG_ENTRY, TAG_EXIT, TAG_PATTERN,
    apply_entry_exit_and_path, apply_42_pattern, build_char_grid,
)

WALL_COLOURS = [
    ("white", curses.COLOR_WHITE),
    ("red", curses.COLOR_RED),
    ("green", curses.COLOR_GREEN),
    ("yellow", curses.COLOR_YELLOW),
    ("blue", curses.COLOR_BLUE),
    ("magenta", curses.COLOR_MAGENTA),
    ("cyan", curses.COLOR_CYAN),
]

PAIR_WALL = 1
PAIR_OPEN = 2
PAIR_PATH = 3
PAIR_ENTRY = 4
PAIR_EXIT = 5
PAIR_STATUS = 6
PAIR_PATTERN = 7


class MazeApp:
    """Holds the loaded maze, view state and display toggles for the TUI."""

    def __init__(self, path: str, config: Any):
        """Store the output file path and config, and load the maze."""
        self.path = path
        self.config = config
        self.show_path = True
        self.show_42 = False
        self.wall_colour_idx = 0
        self.status = "Loaded maze."
        self.top = 0
        self.left = 0
        self.load()

    def load(self) -> None:
        """Parse the output file at self.path into self.maze."""
        self.maze: Maze = parse_output_file(self.path)

    def build_view(self) -> tuple[list[str], list[list[str]]]:
        """Render the current maze into display lines and their style tags."""
        chars, tags = build_char_grid(self.maze)
        apply_42_pattern(chars, tags, self.maze, self.show_42)
        apply_entry_exit_and_path(chars, tags, self.maze, self.show_path)
        lines = ["".join(row) for row in chars]
        return lines, tags

    def regenerate(self) -> None:
        """Generate a new maze, reload it and reset the view, or record failure."""
        try:
            create_maze()
            self.load()
            self.top = 0
            self.left = 0
            self.status = "Maze regenerated."
        except Exception as exc:  # noqa: BLE001
            self.status = f"Regeneration failed: {exc}"

    def cycle_wall_colour(self) -> None:
        """Switch to the next wall colour in WALL_COLOURS."""
        self.wall_colour_idx = (self.wall_colour_idx + 1) % len(WALL_COLOURS)
        name, _ = WALL_COLOURS[self.wall_colour_idx]
        self.status = f"Wall colour: {name}"

    def toggle_path(self) -> None:
        """Toggle whether the solution path is drawn."""
        self.show_path = not self.show_path
        self.status = "Path shown." if self.show_path else "Path hidden."

    def toggle_42(self) -> None:
        """Toggle whether the 42 pattern is drawn."""
        self.show_42 = not self.show_42
        self.status = (
            "42 pattern shown." if self.show_42 else "42 pattern hidden."
        )


def setup_colours(app: MazeApp) -> None:
    """Initialize curses colour pairs, using app's current wall colour choice."""
    curses.start_color()
    curses.use_default_colors()
    _, wall_colour = WALL_COLOURS[app.wall_colour_idx]
    curses.init_pair(PAIR_WALL, wall_colour, -1)
    curses.init_pair(PAIR_OPEN, curses.COLOR_WHITE, -1)
    curses.init_pair(PAIR_PATH, curses.COLOR_YELLOW, -1)
    curses.init_pair(PAIR_ENTRY, curses.COLOR_GREEN, -1)
    curses.init_pair(PAIR_EXIT, curses.COLOR_RED, -1)
    curses.init_pair(PAIR_STATUS, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(PAIR_PATTERN, curses.COLOR_CYAN, -1)


TAG_PAIR = {
    TAG_WALL: PAIR_WALL,
    TAG_OPEN: PAIR_OPEN,
    TAG_PATH: PAIR_PATH,
    TAG_ENTRY: PAIR_ENTRY,
    TAG_EXIT: PAIR_EXIT,
    TAG_PATTERN: PAIR_PATTERN,
}

ATTR_BOLD_TAGS = {TAG_ENTRY, TAG_EXIT, TAG_PATTERN}


def draw(stdscr: "curses.window", app: MazeApp) -> None:
    """Render the visible slice of the maze and the status bar to stdscr."""
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    view_h = max_y - 2  # leave room for the status bar
    view_w = max_x

    lines, tags = app.build_view()
    grid_h = len(lines)
    grid_w = len(lines[0]) if lines else 0

    app.top = max(0, min(app.top, max(0, grid_h - view_h)))
    app.left = max(0, min(app.left, max(0, grid_w - view_w)))

    for screen_r in range(min(view_h, grid_h - app.top)):
        r = screen_r + app.top
        row_chars = lines[r]
        row_tags = tags[r]
        for screen_c in range(min(view_w - 1, grid_w - app.left)):
            c = screen_c + app.left
            ch = row_chars[c]
            tag = row_tags[c]
            pair = TAG_PAIR.get(tag, PAIR_WALL)
            attr = curses.color_pair(pair)
            if tag in ATTR_BOLD_TAGS:
                attr |= curses.A_BOLD
            try:
                stdscr.addstr(screen_r, screen_c, ch, attr)
            except curses.error:
                pass  # bottom-right corner write, safe to ignore

    status = (
        f" [p] path:{'on' if app.show_path else 'off'}  "
        f"[4] 42 pattern:{'on' if app.show_42 else 'off'}  "
        f"[c] wall colour  "
        f"[r] regen  [arrows] scroll  [q] quit  |  {app.status}"
    )
    try:
        stdscr.addstr(
            max_y - 1, 0, status[: max_x - 1].ljust(max_x - 1),
            curses.color_pair(PAIR_STATUS),
        )
    except curses.error:
        pass
    stdscr.refresh()


def _curses_main(stdscr: "curses.window", app: MazeApp) -> None:
    """Run the curses event loop, dispatching keypresses to app actions."""
    curses.curs_set(0)
    setup_colours(app)
    stdscr.keypad(True)

    while True:
        draw(stdscr, app)
        key = stdscr.getch()

        if key in (ord("q"), 27):  # q or ESC
            break
        elif key == ord("p"):
            app.toggle_path()
        elif key == ord("4"):
            app.toggle_42()
        elif key == ord("c"):
            app.cycle_wall_colour()
            setup_colours(app)
        elif key == ord("r"):
            app.regenerate()
        elif key == curses.KEY_UP:
            app.top = max(0, app.top - 1)
        elif key == curses.KEY_DOWN:
            app.top += 1
        elif key == curses.KEY_LEFT:
            app.left = max(0, app.left - 1)
        elif key == curses.KEY_RIGHT:
            app.left += 1


def tui(output_file: str, config: "MazeConfig") -> None:
    """Load output_file and run the interactive maze viewer."""
    app = MazeApp(output_file, config)
    curses.wrapper(lambda stdscr: _curses_main(stdscr, app))
