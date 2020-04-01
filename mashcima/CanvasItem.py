import numpy as np
import cv2
import copy
import random
from typing import List
from mashcima.Sprite import Sprite
from mashcima.Accidental import Accidental
from mashcima.debug import draw_cross


DEBUG_RENDER = False


class CanvasItem:
    """An item that can be placed onto the canvas"""
    def __init__(self, generic_annotation: str):
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

        # generic annotation (note without pitch / rest / barline)
        self.generic_annotation = generic_annotation

        # === NOTE RELATED PROPERTIES ===

        # sprite of the note head
        self.note_head_sprite: Sprite = None

        # sprite of the note stem
        self.note_stem_sprite: Sprite = None

        # if the note has a stem, this is where the beam should be placed
        # (in local pixel coordinates)
        self.stem_head_x = None
        self.stem_head_y = None

        # beam count on either side
        self.beams_left = 0
        self.beams_right = 0

        # sharp, flat, natural, ... (symbol in front of the note)
        self.accidental: Accidental = None

        # duration dot sprite
        self.duration_dot: Sprite = None

        # is this item flipped (rotate 180 deg)
        self.is_flipped = False

    @property
    def is_note(self):
        return self.note_head_sprite is not None

    @property
    def is_beamed(self):
        return self.beams_left > 0 or self.beams_right > 0

    @property
    def is_barline(self):
        return False  # TODO

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

    def prepare_item_for_render(self):
        """Called before rendering - recalculates positions of all important points"""
        self._place_accidental()
        self._place_duration_dot()
        self._recalculate_bounding_box()

    def _place_accidental(self):
        if self.accidental is None:
            return
        # Before this call, accidental is centered on origin
        self.accidental.sprite.x -= self.note_head_sprite.width // 2
        self.accidental.sprite.x -= self.accidental.sprite.width // 2
        self.accidental.sprite.x -= random.randint(5, 25)

    def _place_duration_dot(self):
        if self.duration_dot is None:
            return
        # Before this call, dot is centered on origin
        self.duration_dot.x += self.note_head_sprite.width // 2
        self.duration_dot.x += self.duration_dot.width // 2
        self.duration_dot.x += random.randint(5, 15)
        self.duration_dot.y += random.randint(-5, 5)

    def _recalculate_bounding_box(self):
        effective_sprites = self.sprites
        if self.accidental is not None:
            effective_sprites.append(self.accidental.sprite)
        if self.duration_dot is not None:
            effective_sprites.append(self.duration_dot)
        
        self.left = min([s.x for s in effective_sprites])
        self.right = max([s.x + s.mask.shape[1] for s in effective_sprites])
        self.top = min([s.y for s in effective_sprites])
        self.bottom = max([s.y + s.mask.shape[0] for s in effective_sprites])
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def render(self, img: np.ndarray):
        if DEBUG_RENDER:
            draw_cross(img, self.position_x, self.position_y, 15)
            self._render_bounding_box(img)
            if self.stem_head_x is not None:
                draw_cross(
                    img,
                    self.position_x + self.stem_head_x,
                    self.position_y + self.stem_head_y,
                    5
                )

        for sprite in self.sprites:
            sprite.render(img, self.position_x, self.position_y)

        if self.accidental is not None:
            self.accidental.sprite.render(img, self.position_x, self.position_y)

        if self.duration_dot is not None:
            self.duration_dot.render(img, self.position_x, self.position_y)

    def _render_bounding_box(self, img: np.ndarray):
        cv2.rectangle(
            img,
            (self.left + self.position_x, self.top + self.position_y),
            (self.right + self.position_x, self.bottom + self.position_y),
            color=0.5,
            thickness=1
        )

    def get_annotations(self) -> List[str]:
        # handle notes
        if self.generic_annotation in ["w", "h", "q", "e", "s", "t"]:
            # update apparent generic annotation for beamed notes
            generic_annotation = self.generic_annotation
            if self.is_beamed:
                beams = max(self.beams_left, self.beams_right)
                LETTER_LOOKUP = {1: "e", 2: "s"}
                generic_annotation = LETTER_LOOKUP[beams]
                if self.beams_left == beams:
                    generic_annotation = "=" + generic_annotation
                if self.beams_right == beams:
                    generic_annotation += "="

            # turn generic annotation to a concrete one
            out = [generic_annotation + str(self.note_position)]

            # prepend accidental
            if self.accidental is not None:
                out = [self.accidental.annotation + str(self.note_position)] + out

            return out

        # handle rests
        if self.generic_annotation in ["wr", "hr", "qr", "er", "sr", "tr"]:
            return [self.generic_annotation]

        raise Exception("Given annotation type not implemented")
