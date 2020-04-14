import random
from mashcima import Mashcima
from mashcima.canvas_items.Rest import Rest


class QuarterRest(Rest):
    def get_item_annotation_token(self):
        return "qr"

    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)
        self.sprites.add("rest", random.choice(mc.QUARTER_RESTS).sprites[0])
