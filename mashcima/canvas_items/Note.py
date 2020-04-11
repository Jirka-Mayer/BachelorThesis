from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.Sprite import Sprite
from typing import Dict, List
import numpy as np
import random


class Note(CanvasItem):
    def __init__(self, pitch: int):
        super().__init__()

        # note pitch
        self.pitch = pitch

        # ledger lines
        self._ledger_line_sprites: List[Sprite] = None
        self._ledger_line_y_positions: List[int] = None

    def select_sprites(self, mc: Mashcima):
        self._select_ledger_line_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        out = super().place_item(head, pitch_positions)
        self.sprites.position_y = pitch_positions[self.pitch]
        self._place_ledger_lines(pitch_positions)
        return out
        
    def render(self, img: np.ndarray):
        self._render_ledger_lines(img)
        super().render(img)

    #########################
    # Ledger line rendering #
    #########################

    def _render_ledger_lines(self, img: np.ndarray):
        for i, s in enumerate(self._ledger_line_sprites):
            s.render(
                img,
                self.sprites.position_x,
                self._ledger_line_y_positions[i]
            )

    def _select_ledger_line_sprites(self, mc: Mashcima):
        self._ledger_line_sprites = []
        for p in self._iterate_ledger_line_pitches():
            self._ledger_line_sprites.append(random.choice(mc.LEDGER_LINES))

    def _place_ledger_lines(self, pitch_positions: Dict[int, int]):
        self._ledger_line_y_positions = []
        for p in self._iterate_ledger_line_pitches():
            self._ledger_line_y_positions.append(pitch_positions[p])

    def _iterate_ledger_line_pitches(self):
        if abs(self.pitch) < 6:
            return
        negate = 1 if self.pitch > 0 else -1
        for i in range(6, abs(self.pitch) + 1):
            if i % 2 == 1:
                continue  # odd positions are holes, not lines
            yield i * negate
