import numpy as np
from typing import List, Dict
from mashcima import Mashcima
from mashcima.CanvasItem import CanvasItem
from mashcima.Accidental import Accidental
from mashcima.Sprite import Sprite
from mashcima.Slur import Slur
from mashcima.utils import fork
import app.vocabulary
import cv2
import copy
import random


PITCH_RANGE = app.vocabulary.HIGHEST_POSITION


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

        # canvas item from which a slur is being dragged (when appending)
        self.dragging_slur_from = None

    ##################
    # High level API #
    ##################

    def _generate_note_position(self):
        # TODO: dummy helper
        return random.randint(-PITCH_RANGE, PITCH_RANGE)

    def _generate_accidental(self, accidental: str):
        if accidental is None:
            return None
        assert accidental in ["#", "b", "N"]
        return random.choice(list(
            filter(lambda a: a.annotation == accidental, self.mc.ACCIDENTALS)
        ))

    def add_beamed_group(
            self,
            beams: int = 1,
            notes: int = 2,
            border_beams: int = 0
    ):
        PITCH_CENTER_SPRED = 5
        PITCH_SPRED = 3
        assert PITCH_CENTER_SPRED + PITCH_SPRED <= PITCH_RANGE

        pitch_center = random.randint(-PITCH_CENTER_SPRED, PITCH_CENTER_SPRED)
        for i in range(notes):
            self.append(
                random.choice(self.mc.QUARTER_NOTES),
                note_position=pitch_center + random.randint(-PITCH_SPRED, PITCH_SPRED),
                flip=pitch_center > 0,
                beams_left=(border_beams if i == 0 else beams),
                beams_right=(border_beams if i == notes - 1 else beams),
                accidental=self._generate_accidental()
            )

    def add_beamed_note(
            self,
            pitch: int,
            beam_count: int,
            beam_left: bool,
            beam_right: bool,
            slur_end: bool = False,
            slur_start: bool = False,
            accidental: str = None
    ):
        self.append(
            random.choice(self.mc.QUARTER_NOTES),
            note_position=pitch,
            flip=pitch > 0,
            beams_left=beam_count if beam_left else 0,
            beams_right=beam_count if beam_right else 0,
            accidental=self._generate_accidental(accidental),
            slur_start=slur_start,
            slur_end=slur_end
        )

    def add_quarter_note(
            self,
            pitch: int = None,
            accidental: str = None,
            slur_end: bool = False,
            slur_start: bool = False,
    ) -> CanvasItem:
        pos = self._generate_note_position() if pitch is None else pitch
        return self.append(
            random.choice(self.mc.QUARTER_NOTES),
            note_position=pos,
            flip=pos > 0,
            accidental=self._generate_accidental(accidental=accidental),
            slur_start=slur_start,
            slur_end=slur_end
        )

    def add_quarter_rest(self) -> CanvasItem:
        return self.append(random.choice(self.mc.QUARTER_RESTS))

    def add_half_note(self, pitch: int = None, accidental: str = None) -> CanvasItem:
        pos = self._generate_note_position() if pitch is None else pitch
        return self.append(
            random.choice(self.mc.HALF_NOTES),
            note_position=pos,
            flip=pos > 0,
            accidental=self._generate_accidental(accidental=accidental)
        )

    def add_whole_note(self, pitch: int = None, accidental: str = None) -> CanvasItem:
        return self.append(
            random.choice(self.mc.WHOLE_NOTES),
            note_position=self._generate_note_position() if pitch is None else pitch,
            accidental=self._generate_accidental(accidental=accidental)
        )

    def add_bar_line(self, slur_start=False, slur_end=False) -> CanvasItem:
        return self.append(
            random.choice(self.mc.BAR_LINES),
            slur_start=slur_start,
            slur_end=slur_end
        )

    def add_invisible_barline(self) -> CanvasItem:
        item = self.add_bar_line()
        item.is_invisible = True
        return item

    #################
    # Low level API #
    #################

    def append(
            self,
            item: CanvasItem,
            note_position: int = 0,
            flip: bool = False,
            beams_left: int = 0,
            beams_right: int = 0,
            accidental: Accidental = None,
            duration_dot: Sprite = None,
            slur_end: bool = False,
            slur_start: bool = False,
    ) -> CanvasItem:
        """Adds an item onto the canvas"""
        if slur_end and self.dragging_slur_from is None:
            self.dragging_slur_from = self.add_invisible_barline()

        cp: CanvasItem = copy.deepcopy(item)
        assert not cp.is_flipped
        if flip:
            cp = cp.flipped()
        self.items.append(cp)

        cp.note_position = note_position
        cp.beams_left = beams_left
        cp.beams_right = beams_right
        cp.accidental = copy.deepcopy(accidental)
        cp.duration_dot = copy.deepcopy(duration_dot)

        if slur_end:
            self.add_slur(self.dragging_slur_from, cp)
            self.dragging_slur_from = None
        if slur_start:
            if self.dragging_slur_from is not None:
                raise Exception("Opening slur when one is already being dragged")
            self.dragging_slur_from = cp

        return cp

    def add_slur(self, start_item: CanvasItem, end_item: CanvasItem):
        self.slurs.append(Slur(start_item, end_item))
        start_item.slur_starts = True
        end_item.slur_ends = True

    def render(self):
        from mashcima.generate_staff_lines import generate_staff_lines
        self.img, self.note_positions = generate_staff_lines()

        self._place_items()

        for item in self.items:
            self._render_ledger_lines(item)
            item.render(self.img)

        self._render_beams()

        for s in self.slurs:
            s.render(self.img)

        # crop the result
        self.img = self.img[:, 0:self.head]

        return self.img

    def _render_ledger_lines(self, item: CanvasItem):
        if abs(item.note_position) < 6:
            return
        negate = 1 if item.note_position > 0 else -1
        for i in range(6, abs(item.note_position) + 1):
            if i % 2 == 1:
                continue  # odd positions are holes, not lines
            pos_y = self.note_positions[i * negate]
            sprite = random.choice(self.mc.LEDGER_LINES)
            sprite.render(self.img, item.position_x, pos_y)

    def _render_beams(self):
        beam_thickness = 4
        beam_spacing = 16
        for i in range(len(self.items) - 1):
            this = self.items[i]
            next = self.items[i + 1]
            if this.beams_right <= 0 or next.beams_left <= 0:
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
            if this.beams_right >= 2 and next.beams_left >= 2:
                a, b, m = step_down(a, b, m, this.is_flipped)
                cv2.line(self.img, a, b, thickness=beam_thickness, color=1)

            # render first part of second beam
            if this.beams_right >= 2 and next.beams_left == 1:
                a, b, m = step_down(a, b, m, this.is_flipped)
                cv2.line(self.img, a, m, thickness=beam_thickness, color=1)

            # render second part of second beam
            if this.beams_right == 1 and next.beams_left >= 2:
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

    def get_annotations(self) -> List[str]:
        out: List[str] = []
        for item in self.items:
            out += item.get_annotations()
        return out
