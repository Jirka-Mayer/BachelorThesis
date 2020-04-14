from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
from mashcima.debug import show_images
from typing import List
import numpy as np


mc = Mashcima([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])


def inspect(items: List):
    batch: List[np.ndarray] = []
    BATCH_SIZE = 50
    for index, item in enumerate(items):
        if isinstance(item, Sprite):
            batch.append(item.inspect())
        elif isinstance(item, SpriteGroup):
            batch.append(item.inspect())

        if len(batch) == BATCH_SIZE:
            print("Showing indices:", index - BATCH_SIZE + 1, "-", index, "/", len(items))
            show_images(batch, row_length=10)
            batch = []
    if len(batch) != 0:
        print("Showing indices:", len(items) - len(batch), "-", len(items) - 1, "/", len(items))
        show_images(batch, row_length=10)


###############
# INSPECTIONS #
###############


# inspect(mc.WHOLE_NOTES)
# inspect(mc.QUARTER_NOTES)
# inspect(mc.HALF_NOTES)
#
# inspect(mc.QUARTER_RESTS)
#
# inspect(mc.FLATS)
# inspect(mc.SHARPS)
# inspect(mc.NATURALS)
#
# inspect(mc.DOTS)
# inspect(mc.LEDGER_LINES)
# inspect(mc.BAR_LINES)
