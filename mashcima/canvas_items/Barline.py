from mashcima import Mashcima
from mashcima.canvas_items.SlurableItem import SlurableItem
import random


class Barline(SlurableItem):
    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)
        self.sprites.add("barline", random.choice(mc.BAR_LINES).sprites[0])
