from mashcima import Mashcima
from mashcima.canvas_items.SlurableItem import SlurableItem
import random
import copy


class Barline(SlurableItem):
    def get_item_annotation_token(self):
        return "|"

    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.BAR_LINES))
        super().select_sprites(mc)
