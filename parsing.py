from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Any


class MazeConfig(BaseModel):
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
        parts = value.split(',')
        if len(parts) != 2:
            raise ValueError("Coordinates must be formatted as 'x,y'")
        return int(parts[0].strip()), int(parts[1].strip())

    @field_validator('perfect', mode='before')
    @classmethod
    def perfect_check(cls, value: str) -> bool:
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
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if self.entry == self.exit:
            raise ValueError("Exit coords must be different from entry coords")

        if not (0 <= entry_x < self.width) or not (0 <= entry_y < self.height):
            msg = (f"ENTRY coordinates {self.entry} are out of " +
                   "bounds for a {self.width}x{self.height} maze.")
            raise ValueError(msg)

        if not (0 <= exit_x < self.width) or not (0 <= exit_y < self.height):
            msg = (f"EXIT coordinates {self.exit} are out of bounds for a " +
                   "{self.width}x{self.height} maze.")
            raise ValueError(msg)

        return self


def load_config(filepath: str) -> MazeConfig:
    config_dict: dict[str, Any] = {}

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                config_dict[key.strip().lower()] = val.strip()
    return MazeConfig(**config_dict)
