from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
from typing import List, Optional
import cv2
import sys
import os
import shutil
import numpy as np


def store_sprite(directory: str, symbol_type: str, sprite: Sprite, index: int) -> str:
    """Stores a sprite and returns the corresponding csv line"""
    file_name = "{}.png".format(str(index).rjust(5, "0"))
    path = os.path.join(directory, symbol_type, file_name)
    
    cv2.imwrite(path, (1.0 - sprite.mask) * 255)

    return "{},{},{}".format(
        str(index),
        str(-sprite.x), # invert since we're moving from the global frame
        str(-sprite.y)  # to the sprite's frame of reference
    )


def store_sprites(directory: str, symbol_type: str, sprites: List[Sprite]):
    print("Writing {}...".format(symbol_type))

    os.mkdir(os.path.join(directory, symbol_type))

    with open(os.path.join(directory, symbol_type + ".csv"), "w") as f:
        f.write("index,origin_x,origin_y\n")
        for i in range(len(sprites)):
            line = store_sprite(directory, symbol_type, sprites[i], i)
            f.write(line + "\n")


def convert_sprite_group_to_sprite(sprite_group: SpriteGroup) -> Sprite:
    # single sprite groups are easy to handle
    if len(sprite_group.sprites) == 1:
        return list(sprite_group.sprites.values())[0]

    # multi-sprite groups need to be rendered
    sprite_group.recalculate_bounding_box()
    sprite_group.position_x = -sprite_group.left
    sprite_group.position_y = -sprite_group.top
    mask = np.zeros(
        shape=(sprite_group.height, sprite_group.width),
        dtype=np.float32
    )
    sprite_group.render(mask)
    return Sprite(sprite_group.left, sprite_group.top, mask)


def store_sprite_groups(directory: str, symbol_type: str, sprite_groups: List[SpriteGroup]):
    sprites = [convert_sprite_group_to_sprite(g) for g in sprite_groups]
    store_sprites(directory, symbol_type, sprites)


def print_usage_and_exit(error: Optional[str] = None):
    if error is not None:
        print("Error: " + error)
        print()
    
    print("Usage:")
    print("\t" + "extract_symbols.py [symbols-directory]")
    print()
    print("symbols-directory\tThe directory where to place the extracted symbols")

    exit()


def main():
    if len(sys.argv) != 2:
        print_usage_and_exit()

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print_usage_and_exit("Given path is not a directory")

    # clear the directory
    shutil.rmtree(directory)
    os.mkdir(directory)

    mc = Mashcima(use_cache=True)

    store_sprite_groups(directory, "whole_note", mc.WHOLE_NOTES)
    store_sprite_groups(directory, "half_note", mc.HALF_NOTES)
    store_sprite_groups(directory, "quarter_note", mc.QUARTER_NOTES)
    store_sprite_groups(directory, "eighth_note", mc.EIGHTH_NOTES)
    store_sprite_groups(directory, "sixteenth_note", mc.SIXTEENTH_NOTES)

    store_sprite_groups(directory, "longa_rest", mc.LONGA_RESTS)
    store_sprite_groups(directory, "breve_rest", mc.BREVE_RESTS)
    store_sprite_groups(directory, "whole_rest", mc.WHOLE_RESTS)
    store_sprite_groups(directory, "half_rest", mc.HALF_RESTS)
    store_sprite_groups(directory, "quarter_rest", mc.QUARTER_RESTS)
    store_sprite_groups(directory, "eighth_rest", mc.EIGHTH_RESTS)
    store_sprite_groups(directory, "sixteenth_rest", mc.SIXTEENTH_RESTS)

    store_sprites(directory, "sharp", mc.SHARPS)
    store_sprites(directory, "flat", mc.FLATS)
    store_sprites(directory, "natural", mc.NATURALS)
    store_sprites(directory, "dot", mc.DOTS)
    store_sprites(directory, "ledger_line", mc.LEDGER_LINES)

    store_sprite_groups(directory, "bar_line", mc.BAR_LINES)
    store_sprite_groups(directory, "tall_bar_line", mc.TALL_BAR_LINES)
    store_sprite_groups(directory, "g_clef", mc.G_CLEFS)
    store_sprite_groups(directory, "f_clef", mc.F_CLEFS)
    store_sprite_groups(directory, "c_clef", mc.C_CLEFS)

    for key in mc.TIME_MARKS:
        store_sprite_groups(
            directory,
            "time_mark_" + key[len("time_"):],
            mc.TIME_MARKS[key]
        )


main()
