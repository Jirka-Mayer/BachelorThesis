from typing import List
from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.canvas_items.InvisibleSlurEnd import InvisibleSlurEnd
from mashcima.canvas_items.BeamedNote import BeamedNote
from mashcima.Slur import Slur
from mashcima.Beam import Beam
import random


class Canvas:
    def __init__(self):
        # items on the canvas
        self.items: List[CanvasItem] = []

        # beams between beamed notes
        self.beams: List[Beam] = []

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

        self._create_beams()
        self._create_slurs()

    def _create_beams(self):
        self.beams = []

        in_beam = False
        beam_items = []
        for i in self.items:
            if not isinstance(i, BeamedNote):
                continue

            if in_beam:
                # append item to a built beam
                beam_items.append(i)

                # end the beam
                if not i.right_beamed:
                    self.beams.append(Beam(beam_items))
                    in_beam = False
                    beam_items = []

            else:
                # start new beam
                if i.right_beamed:
                    beam_items.append(i)
                    in_beam = True

    def _create_slurs(self):
        self.slurs = []
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

        # select sprites
        for item in self.items:
            item.select_sprites(mc)

        from mashcima.generate_staff_lines import generate_staff_lines
        img, pitch_positions = generate_staff_lines()

        # place sprites and place items
        head = self._place_items(pitch_positions)

        # place beams
        for b in self.beams:
            b.place()

        # render
        for item in self.items:
            item.render(img)

        for b in self.beams:
            b.render(img)

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
