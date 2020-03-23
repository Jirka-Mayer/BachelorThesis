import numpy as np
from typing import List, Dict
from mashcima import Mashcima


class GeneratorState:
    """Represents state of the mashcima at some point
    in time during generation"""
    def __init__(self, mc: Mashcima):
        # mashcima reference
        self.mc = mc

        # generated staff image
        self.img: np.ndarray = None

        # mapping from note position to pixel position
        self.note_positions: Dict[int, int] = {}

        # label for the generated data item
        self.annotation: List[str] = []

        # printer head position in pixels (what has already been printed)
        self.head = 0

        from mashcima.generate_staff_lines import generate_staff_lines
        self.img, self.note_positions = generate_staff_lines()
