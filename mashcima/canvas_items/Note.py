from mashcima import Mashcima
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.Sprite import Sprite
from typing import Dict, List, Tuple, Optional
import numpy as np
import random


class Note(SlurableItem):
    def __init__(self, pitch: int, accidental: Optional[str], **kwargs):
        super().__init__(**kwargs)

        # note pitch
        self.pitch = pitch

        # accidental attachment type
        self.accidental = accidental
        assert accidental in [None, "#", "b", "N"]

        # ledger lines
        self._ledger_line_sprites: List[Sprite] = None
        self._ledger_line_y_positions: List[int] = None

    def get_item_annotation_token(self):
        return self.get_note_generic_annotation() + str(self.pitch)

    def get_note_generic_annotation(self) -> str:
        raise NotImplementedError("Override this")

    def get_before_attachment_tokens(self) -> List[str]:
        tokens = super().get_before_attachment_tokens()
        if self.accidental is not None:
            tokens = [self.accidental + str(self.pitch)] + tokens
        return tokens

    def get_after_attachment_tokens(self) -> List[str]:
        tokens = super().get_after_attachment_tokens()
        return tokens

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

    ##########################
    # Slur attachment points #
    ##########################

    def get_slur_start_attachment_point(self, slur) -> Tuple[int, int]:
        if slur.tail_to_tail:
            return self._get_slur_after_note_attachment_point()
        else:
            return self._get_slur_below_note_attachment_point(slur)

    def get_slur_end_attachment_point(self, slur) -> Tuple[int, int]:
        if slur.tail_to_tail:
            return self._get_slur_before_note_attachment_point()
        else:
            return self._get_slur_below_note_attachment_point(slur)

    def _get_slur_after_note_attachment_point(self):
        return (
            self.sprites.position_x + (self.sprites.sprite("notehead").width // 2 + 8),
            self.sprites.position_y
        )

    def _get_slur_before_note_attachment_point(self):
        return (
            self.sprites.position_x - (self.sprites.sprite("notehead").width // 2 + 8),
            self.sprites.position_y
        )

    def _get_slur_below_note_attachment_point(self, slur):
        """Below or above if the note is flipped"""
        sign = (-1 if slur.flipped else 1)
        return (
            self.sprites.position_x,
            self.sprites.position_y + sign * (self.sprites.sprite("notehead").height // 2 + 8)
        )
