from mashcima import Mashcima
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.Sprite import Sprite
from typing import Dict, List, Tuple, Optional
import numpy as np
import random
import copy


class Note(SlurableItem):
    def __init__(
            self,
            pitch: int = 0,
            accidental: Optional[str] = None,
            duration_dots: Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        # note pitch
        self.pitch = pitch

        # accidental attachment type
        assert accidental in [None, "#", "b", "N"]
        self.accidental = accidental

        # duration dots
        assert duration_dots in [None, "*", "**"]
        self.duration_dots = duration_dots

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
        if self.duration_dots is not None:
            tokens = tokens + [self.duration_dots]
        return tokens

    def select_sprites(self, mc: Mashcima):
        self._select_ledger_line_sprites(mc)
        self._select_accidental_sprite(mc)
        self._select_duration_dot_sprites(mc)

    def place_sprites(self):
        self._place_accidental()
        self._place_duration_dots()
        super().place_sprites()

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

    ########################
    # Accidental rendering #
    ########################

    def _select_accidental_sprite(self, mc: Mashcima):
        if self.accidental is None:
            return
        sprite = None
        if self.accidental == "#":
            sprite = copy.deepcopy(random.choice(mc.SHARPS))
        if self.accidental == "b":
            sprite = copy.deepcopy(random.choice(mc.FLATS))
        if self.accidental == "N":
            sprite = copy.deepcopy(random.choice(mc.NATURALS))
        assert sprite is not None
        self.sprites.add("accidental", sprite)

    def _place_accidental(self):
        if self.accidental is None:
            return
        # Before this call, accidental is centered on origin
        sprite = self.sprites.sprite("accidental")
        sprite.x -= self.sprites.sprite("notehead").width // 2
        sprite.x -= sprite.width // 2
        sprite.x -= random.randint(5, 25)

    ##########################
    # Duration dot rendering #
    ##########################

    def _select_duration_dot_sprites(self, mc: Mashcima):
        if self.duration_dots is None:
            return
        self.sprites.add("duration_dot", copy.deepcopy(random.choice(mc.DOTS)))
        if self.duration_dots == "**":
            self.sprites.add("duration_dot_2", copy.deepcopy(random.choice(mc.DOTS)))

    def _place_duration_dots(self):
        if self.duration_dots is None:
            return
        # Before this call, dot is centered on origin
        first_dot = self.sprites.sprite("duration_dot")
        first_dot.x += self.sprites.sprite("notehead").width // 2
        first_dot.x += first_dot.width // 2
        first_dot.x += random.randint(5, 15)
        if self.pitch % 2 == 0:
            first_dot.y += 10 if self.pitch > 0 else -10  # put it into a space
        first_dot.y += random.randint(-5, 5)
        if self.duration_dots == "**":
            second_dot = self.sprites.sprite("duration_dot_2")
            second_dot.x += first_dot.x
            second_dot.y += first_dot.y
            second_dot.x += second_dot.width // 2
            second_dot.x += random.randint(5, 15)

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