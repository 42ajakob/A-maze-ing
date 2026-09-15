from sys import argv, exit
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, field_validator, model_validator


class ConfigKey(Enum):
    """Required Keys from config file"""
    SEED = "SEED"
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"


class MazeConfig(BaseModel):
    """Stores and validates the values"""
    seed: int = Field(..., ge=0)
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    maze_entry: tuple[int, int] = Field(...)
    maze_exit: tuple[int, int] = Field(...)
    output_file: str = Field(...)
    perfect: bool = Field(...)

    @field_validator("maze_entry", "maze_exit")
    @classmethod
    def coords_non_negative(cls, v: tuple[int, int]) -> tuple[int, int]:
        """Checks maze_entry and maze_exit to have non negative numbers"""
        if any(val < 0 for val in v):
            raise ValueError("Input should be greater than or equal to 0")
        return v

    @model_validator(mode="after")
    def check_bounds(self) -> "MazeConfig":
        """Checks maze_entry and maze_exit to be in bounds of the maze"""
        for name, (x, y) in (
            ("maze_entry", self.maze_entry),
            ("maze_exit", self.maze_exit),
        ):
            if not (0 <= x <= self.width and 0 <= y <= self.height):
                raise ValueError(
                    f"{name} {(x, y)} is out of bounds for "
                    f"width={self.width}, height={self.height}"
                )
        return self


def parse_config() -> dict[ConfigKey, str]:
    """Searches for all key, value pairs
    and makes sure the config file is valid
    """
    found_keys = {}

    if len(argv) < 2:
        print("Error: missing config file argument")
        exit(2)

    try:
        config_file = open(argv[1])
    except OSError as e:
        print(f"Error: cannot open config file {argv[1]!r}: {e}")
        exit(1)

    with config_file as file:
        for lineno, raw_line in enumerate(file.read().splitlines(), start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue
            elif "=" not in line:
                print(f"Line {lineno}: invalid line: {raw_line}")
                exit(3)

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            try:
                enum_key = ConfigKey[key]
            except KeyError:
                print(f"Line {lineno}: unknown key: {key}")
                exit(4)

            found_keys[enum_key] = value

        missing = set(ConfigKey) - set(found_keys.keys())
        if missing:
            print(f"Error: missing keys: {[m.name for m in missing]}")
            exit(5)

        return found_keys


def build_class(found_keys: dict[ConfigKey, str]) -> MazeConfig:
    """Builds MazeConfig class"""
    kwargs: dict[str, Any] = {}
    for key, value in found_keys.items():
        if key is ConfigKey.ENTRY:
            kwargs["maze_entry"] = tuple(int(v) for v in value.split(","))
        elif key is ConfigKey.EXIT:
            kwargs["maze_exit"] = tuple(int(v) for v in value.split(","))
        else:
            kwargs[key.name.lower()] = value

    return MazeConfig.model_validate(kwargs)


def parser() -> "MazeConfig":
    """Find Keys, build MazeConfig and return it"""
    found_keys = parse_config()
    try:
        maze_config = build_class(found_keys)
    except ValueError as e:
        msg = str(e).split(" [type=")[0]
        print(f"Error: {msg}")
        exit(6)
    return maze_config
