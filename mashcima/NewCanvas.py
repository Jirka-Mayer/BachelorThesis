import numpy as np
from typing import List, Dict
from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.canvas_items.InvisibleSlurEnd import InvisibleSlurEnd
from mashcima.Accidental import Accidental
from mashcima.Sprite import Sprite
from mashcima.Slur import Slur
from mashcima.utils import fork
import app.vocabulary
import cv2
import copy
import random


class Canvas:
    def __init__(self):
        # items on the canvas
        self.items: List[CanvasItem] = []

        # slurs between items
        self.slurs: List[Slur] = []

        # was the construction finished or not
        self._construction_finished = False
        
    def add(self, item: CanvasItem):
        if self._construction_finished:
            raise Exception("Cannot add item, construction has been finished")
        self.items.append(item)

    def get_annotations(self) -> List[str]:
        out: List[str] = []
        for item in self.items:
            out += item.get_annotation_tokens()
        return out

    def finish_construction(self):
        """Creates additional data structures around canvas items"""
        if self._construction_finished:
            raise Exception("Construction has been already finished")

        self._create_slurs()

    def _create_slurs(self):
        slur_stack: List[SlurableItem] = []

        def add_slur(start: SlurableItem, end: SlurableItem):
            self.slurs.append(Slur(start, end))

        def create_invisible_slur_end(at_index: int, start_here: bool) -> SlurableItem:
            ise = InvisibleSlurEnd(
                slur_end=not start_here,
                slur_start=start_here
            )
            self.items.insert(at_index, ise)
            return ise

        # iterate over slurable items
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if isinstance(item, SlurableItem):

                if item.slur_end:
                    if len(slur_stack) == 0:  # slur ending out of nowhere
                        slur_stack.append(create_invisible_slur_end(i, True))
                        i += 1
                    add_slur(slur_stack.pop(), item)

                if item.slur_start:
                    slur_stack.append(item)

                pass  # here do something

            i += 1

        # slurs not ending anywhere
        while len(slur_stack) != 0:
            start = slur_stack.pop()
            end = create_invisible_slur_end(self.items.index(start) + 1, False)
            add_slur(start, end)

    def render(self, mc: Mashcima):
        if not self._construction_finished:
            self.finish_construction()

        for item in self.items:
            item.select_sprites(mc)

        from mashcima.generate_staff_lines import generate_staff_lines
        img, pitch_positions = generate_staff_lines()

        head = self._place_items(pitch_positions)

        for item in self.items:
            item.render(img)

        print("TODO: render beams")
        #self._render_beams()

        for s in self.slurs:
            s.render(img)

        # crop the result
        img = img[:, 0:head]

        return img

    def _place_items(self, pitch_positions):
        """Move items to proper places in the pixel space"""
        for item in self.items:
            item.place_sprites()

        def generate_padding():
            return random.randint(5, 25)

        head = 0
        for i, item in enumerate(self.items):
            head += generate_padding()  # left padding
            head += item.place_item(head, pitch_positions)
            head += generate_padding()  # right padding
        return head

    # def _render_beams(self):
    #     beam_thickness = 4
    #     beam_spacing = 16
    #     for i in range(len(self.items) - 1):
    #         this = self.items[i]
    #         next = self.items[i + 1]
    #         if this.beams_right <= 0 or next.beams_left <= 0:
    #             continue
    #
    #         # render the whole first beam
    #         a = (this.position_x + this.stem_head_x, this.position_y + this.stem_head_y)
    #         b = (next.position_x + next.stem_head_x, next.position_y + next.stem_head_y)
    #         m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
    #         cv2.line(self.img, a, b, thickness=beam_thickness, color=1)
    #
    #         def step_down(a, b, m, flip):
    #             sp = -beam_spacing if flip else beam_spacing
    #             return (a[0], a[1] + sp), (b[0], b[1] + sp), (m[0], m[1] + sp)
    #
    #         # render whole second beam
    #         if this.beams_right >= 2 and next.beams_left >= 2:
    #             a, b, m = step_down(a, b, m, this.is_flipped)
    #             cv2.line(self.img, a, b, thickness=beam_thickness, color=1)
    #
    #         # render first part of second beam
    #         if this.beams_right >= 2 and next.beams_left == 1:
    #             a, b, m = step_down(a, b, m, this.is_flipped)
    #             cv2.line(self.img, a, m, thickness=beam_thickness, color=1)
    #
    #         # render second part of second beam
    #         if this.beams_right == 1 and next.beams_left >= 2:
    #             a, b, m = step_down(a, b, m, next.is_flipped)
    #             cv2.line(self.img, m, b, thickness=beam_thickness, color=1)
