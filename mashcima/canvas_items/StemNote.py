from mashcima.canvas_items.Note import Note
from mashcima.debug import draw_cross
import numpy as np


class StemNote(Note):
    def __init__(self, pitch: int, **kwargs):
        super().__init__(pitch, **kwargs)

        # is the note flipped upside-down?
        self.flipped = pitch > 0

    @property
    def stem_head_x(self):
        return self.sprites.point("stem_head")[0]

    @property
    def stem_head_y(self):
        return self.sprites.point("stem_head")[1]

    def place_sprites(self):
        if self.flipped:
            self.sprites = self.sprites.create_flipped_copy()
        super().place_sprites()

    def render(self, img: np.ndarray):
        super().render(img)

        if self.DEBUG_RENDER:
            draw_cross(
                img,
                self.sprites.position_x + self.stem_head_x,
                self.sprites.position_y + self.stem_head_y,
                5
            )
