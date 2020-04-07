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

        # unless one is barline, then take the flip of the note
        if self.start_item.is_barline:
            self.is_flipped = self.end_item.is_flipped
        if self.end_item.is_barline:
            self.is_flipped = self.start_item.is_flipped

    @property
    def _is_crossed(self):
        if self.start_item.is_barline or self.end_item.is_barline:
            return False
        return self.start_item.is_flipped != self.end_item.is_flipped

    def _get_attachment_point(self, item: CanvasItem):
        if item.is_note:
            if self._is_crossed:
                if item == self.start_item:
                    return self._get_after_note_attachment_point(item)
                else:
                    return self._get_before_note_attachment_point(item)
            else:
                return self._get_below_note_attachment_point(item)
        if item.is_barline:
            sign = -1 if item == self.start_item else 1
            y = self.end_item.position_y if item == self.start_item else self.start_item.position_y
            return (
                item.position_x + sign * (item.sprites[0].width // 2 + 8),
                y
            )
        raise Exception("Slur has to end on a note or barline only")

    def _get_after_note_attachment_point(self, item: CanvasItem):
        assert item.is_note
        return (
            item.position_x + (item.note_head_sprite.width // 2 + 8),
            item.position_y
        )

    def _get_before_note_attachment_point(self, item: CanvasItem):
        assert item.is_note
        return (
            item.position_x - (item.note_head_sprite.width // 2 + 8),
            item.position_y
        )

    def _get_below_note_attachment_point(self, item: CanvasItem):
        """Below or above if the note is flipped"""
        assert item.is_note
        sign = (-1 if self.is_flipped else 1)
        return (
            item.position_x,
            item.position_y + sign * (item.note_head_sprite.height // 2 + 8)
        )

    def render(self, img: np.ndarray):
        slur_thickness = 3

        # NOTE: the slur is rendered as a parabola going through 3 points
        # (two attachments and one center point)

        self._set_is_flipped()
        start_attachment = self._get_attachment_point(self.start_item)
        end_attachment = self._get_attachment_point(self.end_item)
        width = end_attachment[0] - start_attachment[0]

        # calculate center point
        center_point = [
            (start_attachment[0] + end_attachment[0]) // 2,
            (start_attachment[1] + end_attachment[1]) // 2
        ]
        center_point[1] += (-1 if self.is_flipped else 1) * min(int(width / 5), 20)
        center_point = tuple(center_point)

        # calculate coefficients a of: y = ax^2 +bx +c
        A = np.array([
            [start_attachment[0] ** 2, start_attachment[0], 1],
            [center_point[0] ** 2, center_point[0], 1],
            [end_attachment[0] ** 2, end_attachment[0], 1]
        ])
        v = np.array([
            [start_attachment[1]],
            [center_point[1]],
            [end_attachment[1]]
        ])
        abc = np.linalg.inv(A).dot(v)
        f = lambda x: abc[0] * x**2 + abc[1] * x + abc[2]

        for x in range(start_attachment[0], end_attachment[0]):
            cv2.line(
                img,
                (x, f(x)),
                (x + 1, f(x + 1)),
                thickness=slur_thickness,
                color=1
            )
