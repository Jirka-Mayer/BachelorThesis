import numpy as np
from typing import List, Dict
from mashcima import Mashcima
from mashcima.CanvasItem import CanvasItem
from mashcima.Accidental import Accidental
from mashcima.Sprite import Sprite
from mashcima.Slur import Slur
import cv2
import copy
import random


class Canvas:
    """Represents the canvas that the generator writes onto"""
    def __init__(self, mc: Mashcima):
        # mashcima reference
        self.mc = mc

        # items on the canvas
        self.items: List[CanvasItem] = []

        # slurs between items
        self.slurs: List[Slur] = []

        # === state used for canvas rendering ===

        # the image that is being drawn onto
        self.img: np.ndarray = None

        # mapping from note position to pixel position
        self.note_positions: Dict[int, int] = {}

        # item placing head (x coordinate)
        self.head = 0

    def append(
            self,
            item: CanvasItem,
            note_position: int = 0,
            flip: bool = False,
            beam: int = 0,
            accidental: Accidental = None,
            duration_dot: Sprite = None
    ):
        """Adds an item onto the canvas"""
        cp: CanvasItem = copy.deepcopy(item)
        assert not cp.is_flipped
        if flip:
            cp = cp.flipped()
        self.items.append(cp)

        cp.note_position = note_position
        cp.beam = beam
        cp.accidental = copy.deepcopy(accidental)
        cp.duration_dot = copy.deepcopy(duration_dot)

    def add_slur(self, start_item: CanvasItem, end_item: CanvasItem):
        self.slurs.append(Slur(start_item, end_item))

    def render(self):
        from mashcima.generate_staff_lines import generate_staff_lines
        self.img, self.note_positions = generate_staff_lines()

        self._place_items()

        for item in self.items:
            item.render(self.img)

        self._render_beams()

        for s in self.slurs:
            s.render(self.img)

        return self.img

    def _render_beams(self):
        beam_thickness = 4
        beam_spacing = 16
        for i in range(len(self.items) - 1):
            this = self.items[i]
            next = self.items[i + 1]
            if this.beam <= 0 or next.beam <= 0:
                continue

            # render the whole first beam
            a = (this.position_x + this.stem_head_x, this.position_y + this.stem_head_y)
            b = (next.position_x + next.stem_head_x, next.position_y + next.stem_head_y)
            m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
            cv2.line(self.img, a, b, thickness=beam_thickness, color=1)

            def step_down(a, b, m, flip):
                sp = -beam_spacing if flip else beam_spacing
                return (a[0], a[1] + sp), (b[0], b[1] + sp), (m[0], m[1] + sp)

            # render whole second beam
            if this.beam >= 2 and next.beam >= 2:
                a, b, m = step_down(a, b, m, this.is_flipped)
                cv2.line(self.img, a, b, thickness=beam_thickness, color=1)

            # render first part of second beam
            if this.beam >= 2 and next.beam == 1:
                a, b, m = step_down(a, b, m, this.is_flipped)
                cv2.line(self.img, a, m, thickness=beam_thickness, color=1)

            # render second part of second beam
            if this.beam == 1 and next.beam >= 2:
                a, b, m = step_down(a, b, m, next.is_flipped)
                cv2.line(self.img, m, b, thickness=beam_thickness, color=1)

    def _place_items(self):
        """Move items to proper places in the pixel space"""
        for item in self.items:
            item.prepare_item_for_render()

        def generate_padding():
            return random.randint(5, 25)

        self.head = 0
        for i, item in enumerate(self.items):
            padding_left = generate_padding()
            padding_right = generate_padding()
            item.position_x = self.head + padding_left - item.left
            item.position_y = self.note_positions[item.note_position]
            self.head += padding_left + item.width + padding_right
