"""Provide classes to generate, solve and visualize perfect or imperfect mazes.

This package exports the functionality required to initialize a grid of cells,
generate a valid maze structure (preventing open 3x3 areas and embedding a
central '42' display), and calculate the shortest path from entry to exit.

Classes:
    Cell: Hold information about an individual cell in the maze.
    MazeGenerator: Generate a maze and find the shortest path to the exit.
"""

from .maze import Cell, MazeGenerator

__all__ = ['Cell', 'MazeGenerator']
__author__ = "Bilal El Azzouzi, Lindsay Moreau"
