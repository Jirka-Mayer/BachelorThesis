from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from typing import Optional, Dict
import random
import copy


class Rest(CanvasItem):
    def __init__(
            self,
            rest_kind: str = "qr",
            duration_dots: Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        # rest kind
        assert rest_kind in ["wr", "hr", "qr", "er", "sr"]
        self.kind = rest_kind

        # duration dots
        assert duration_dots in [None, "*", "**"]
        self.duration_dots = duration_dots
        assert duration_dots is None  # TODO: duration dots not yet implemented for rests

    def get_item_annotation_token(self) -> str:
        return self.kind

    def contribute_to_padding(self):
        if self.kind in ["wr", "hr"]:
            self.sprites.padding_left += 20
            self.sprites.padding_right += 20

    def select_sprites(self, mc: Mashcima):
        if self.kind == "wr":
            self.sprites = copy.deepcopy(random.choice(mc.WHOLE_RESTS))
        if self.kind == "hr":
            self.sprites = copy.deepcopy(random.choice(mc.HALF_RESTS))
        if self.kind == "qr":
            self.sprites = copy.deepcopy(random.choice(mc.QUARTER_RESTS))
        if self.kind == "er":
            self.sprites = copy.deepcopy(random.choice(mc.EIGHTH_RESTS))
        if self.kind == "sr":
            self.sprites = copy.deepcopy(random.choice(mc.SIXTEENTH_RESTS))
        super().select_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]):
        out = super().place_item(head, pitch_positions)
        if self.kind == "wr":
            self.sprites.position_y = pitch_positions[2]
        return out
