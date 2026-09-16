"""Functions related to the 42 pattern."""


def get_42_pattern(width: int, height: int) -> set[tuple[int, int]]:
    """Return the centered maze-cell coordinates for the 42 pattern."""
    pattern = {
        (0, 0),
        (2, 0),
        (0, 1),
        (2, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 3),
        (2, 4),

        (4, 0),
        (5, 0),
        (6, 0),
        (6, 1),
        (4, 2),
        (5, 2),
        (6, 2),
        (4, 3),
        (4, 4),
        (5, 4),
        (6, 4),
    }

    if width < 7 or height < 5:
        return set()

    pattern_width = 7
    pattern_height = 5

    offset_x = (width - pattern_width) // 2
    offset_y = (height - pattern_height) // 2

    return {
        (x + offset_x, y + offset_y)
        for x, y in pattern
    }
