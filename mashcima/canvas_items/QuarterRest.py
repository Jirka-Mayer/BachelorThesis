import random
from mashcima import Mashcima
from mashcima.canvas_items.Rest import Rest
import copy


class QuarterRest(Rest):
    def get_item_annotation_token(self):
        return "qr"

    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.QUARTER_RESTS))
        super().select_sprites(mc)
