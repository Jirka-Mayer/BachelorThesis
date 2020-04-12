from mashcima import Mashcima
from mashcima.canvas_items.QuarterNote import QuarterNote
from mashcima.Sprite import Sprite
from typing import Dict, List, Tuple
import numpy as np
import random


class BeamedNote(QuarterNote):
    def __init__(self, beams: int, left_beamed: bool, right_beamed: bool, **kwargs):
        super().__init__(**kwargs)
        assert beams in [1, 2, 3]

        self.beams = beams
        self.left_beamed = left_beamed
        self.right_beamed = right_beamed

    def get_annotation_tokens(self):
        SYMBOLS = {
            1: "e",
            2: "s",
            3: "t"
        }
        token = SYMBOLS[self.beams]
        if self.left_beamed:
            token = "=" + token
        if self.right_beamed:
            token += "="
        return [token + str(self.pitch)]
