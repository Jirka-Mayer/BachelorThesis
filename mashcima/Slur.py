import numpy as np
import cv2
import random
from mashcima.CanvasItem import CanvasItem


class Slur:
    def __init__(self, start_item: CanvasItem, end_item: CanvasItem):
        assert start_item.is_note or start_item.is_barline
        assert end_item.is_note or end_item.is_barline
        self.start_item = start_item
        self.end_item = end_item

        # True: /\   False: \/
        self.is_flipped = False

    def _set_is_flipped(self):
        # both not flipped
        if not self.start_item.is_flipped and not self.end_item.is_flipped:
            self.is_flipped = False
            return

        # both flipped
        if self.start_item.is_flipped and self.end_item.is_flipped:
            self.is_flipped = True
            return

        # otherwise randomize
        self.is_flipped = random.choice([True, False])

    def _get_attachment_point(self, item: CanvasItem):
        # TODO: dummy implementation
        return item.position_x, item.position_y + item.note_head_sprite.height // 2 + 5

    def render(self, img: np.ndarray):
        slur_thickness = 3

        self._set_is_flipped()
        start_attachment = self._get_attachment_point(self.start_item)
        end_attachment = self._get_attachment_point(self.end_item)

        cv2.line(
            img,
            start_attachment,
            end_attachment,
            thickness=slur_thickness,
            color=1
        )
