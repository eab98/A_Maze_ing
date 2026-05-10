"""This module handles the parsing of the configuration file."""
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Any


class MazeConfig(BaseModel):
    """Hold parsed configuration values from the configuration file.

    Parse the configuration file using pydantic and hold values if
    parsing is successful. Raise exceptions otherwise.
    """
    width: int = Field(..., gt=1)
    height: int = Field(..., gt=1)
    entry: tuple[int, int] = Field(...)
    exit: tuple[int, int] = Field(...)
    output_file: str = Field(..., min_length=1)
    perfect: bool = Field(...)
    seed: int | None = Field(default=None)

    @field_validator('entry', 'exit', mode='before')
    @classmethod
    def parse_coordinates(cls, value: str) -> tuple[int, int]:
        """Check that coordinates are correctly formatted."""
        parts = value.split(',')
        if len(parts) != 2:
            raise ValueError("Coordinates must be formatted as 'x,y'")
        return int(parts[0].strip()), int(parts[1].strip())

    @field_validator('perfect', mode='before')
    @classmethod
    def perfect_check(cls, value: str) -> bool:
        """Check that the perfect boolean is true or false."""
        val_lower = value.strip().lower()
        if val_lower == 'true':
            return True
        elif val_lower == 'false':
            return False
        else:
            msg = "PERFECT must be 'true' or 'false' (case-insensitive)"
            raise ValueError(msg)

    @model_validator(mode='after')
    def check_coordinates(self) -> 'MazeConfig':
        """Check that entry and exit are within bounds and not equals."""
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if self.entry == self.exit:
            raise ValueError("Exit coords must be different from entry coords")

        if not (0 <= entry_x < self.width) or not (0 <= entry_y < self.height):
            msg = (f"ENTRY coordinates {self.entry} are out of " +
                   f"bounds for a {self.width}x{self.height} maze.")
            raise ValueError(msg)

        if not (0 <= exit_x < self.width) or not (0 <= exit_y < self.height):
            msg = (f"EXIT coordinates {self.exit} are out of bounds for a " +
                   f"{self.width}x{self.height} maze.")
            raise ValueError(msg)

        return self


def load_config(filepath: str) -> MazeConfig:
    """Read the content of the configuration file.

    Argument:
    filepath: the path to the configuration file.

    Return:
        A MazeConfig object holding the parsed configuration.
    Raises:
        FileNotFoundError: Raised if config file cannot be found.
        PermissionError: Raised if config file cannot be accessed.
    """
    config_dict: dict[str, Any] = {}

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    conf_key = key.strip().lower()
                    if conf_key in config_dict.keys():
                        msg = f"Field {conf_key} is repeated in the config file"
                        raise ValueError(msg)
                    config_dict[key.strip().lower()] = val.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"{filepath} could not be found")
    except PermissionError:
        raise PermissionError(f"{filepath} could not be accessed")
    return MazeConfig(**config_dict)
