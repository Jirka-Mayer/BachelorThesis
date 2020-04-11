from mashcima import Mashcima
from mashcima.canvas_items.StemNote import StemNote
import random


class HalfNote(StemNote):
    def get_annotation_tokens(self):
        return ["h" + str(self.pitch)]

    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)
        hn = random.choice(mc.HALF_NOTES)
        self.sprites.add("notehead", hn.sprites[0])
        self.sprites.add("stem", hn.sprites[1])
        self.sprites.add_point("stem_head", (hn.stem_head_x, hn.stem_head_y))
