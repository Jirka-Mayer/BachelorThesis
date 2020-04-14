from mashcima import Mashcima
from mashcima.canvas_items.Note import Note
import random


class WholeNote(Note):
    def get_note_generic_annotation(self) -> str:
        return "w"
    
    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)
        self.sprites.add("notehead", random.choice(mc.WHOLE_NOTES).sprites[0])
