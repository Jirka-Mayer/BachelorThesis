import numpy as np
import cv2
import copy
from typing import List
from mashcima.Sprite import Sprite


DEBUG_RENDER = True


class CanvasItem:
    """An item that can be placed onto the canvas"""
    def __init__(self):
        # position of this symbol in canvas pixel coordinates
        self.position_x = 0
        self.position_y = 0

        # bounding box in local pixel space
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0
        self.width = 0
        self.height = 0

        # list of sprites to be drawn
        self.sprites: List[Sprite] = []

        # position in the note-pitch dimension
        self.note_position = 0

        # if the note has a stem, this is where the beam should be placed
        # (in local pixel coordinates)
        self.stem_head_x = None
        self.stem_head_y = None

        # beam count (0, 1, 2 are the only options)
        self.beam = 0

        # is this item flipped (rotate 180 deg)
        self.is_flipped = False

    def flipped(self):
        """Returns a flipped copy of this item"""
        cp = copy.deepcopy(self)

        if self.stem_head_x is not None:
            cp.stem_head_x = -self.stem_head_x
            cp.stem_head_y = -self.stem_head_y

        for sprite in cp.sprites:
            sprite.flip()

        cp.is_flipped = not self.is_flipped

        return cp

    def add_sprite(self, sprite: Sprite):
        self.sprites.append(sprite)

    def recalculate_bounding_box(self):
        self.left = min([s.x for s in self.sprites])
        self.right = max([s.x + s.mask.shape[1] for s in self.sprites])
        self.top = min([s.y for s in self.sprites])
        self.bottom = max([s.y + s.mask.shape[0] for s in self.sprites])
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def render(self, img: np.ndarray):
        if DEBUG_RENDER:
            self._render_cross(img, self.position_x, self.position_y, 15)
            self._render_bounding_box(img)
            if self.stem_head_x is not None:
                self._render_cross(
                    img,
                    self.position_x + self.stem_head_x,
                    self.position_y + self.stem_head_y,
                    5
                )
        for sprite in self.sprites:
            sprite.render(img, self.position_x, self.position_y)

    def _render_cross(self, img: np.ndarray, x, y, size: int):
        cv2.line(
            img,
            (x - size, y + size),
            (x + size, y - size),
            thickness=2,
            color=0.5
        )
        cv2.line(
            img,
            (x - size, y - size),
            (x + size, y + size),
            thickness=2,
            color=0.5
        )

    def _render_bounding_box(self, img: np.ndarray):
        cv2.rectangle(
            img,
            (self.left + self.position_x, self.top + self.position_y),
            (self.right + self.position_x, self.bottom + self.position_y),
            color=0.5,
            thickness=1
        )
