import numpy as np
from mashcima.utils import has_outlink_to, get_outlink_to
from mashcima.CompositeObject import CompositeObject
from mashcima import Mashcima
from mashcima.CanvasItem import CanvasItem
from mashcima.Sprite import Sprite


def _build_notehead_stem_pairs(noteheads, stems):
    """
        Combines list of noteheads and a list of stems into a list of
        can vas items. Handles flipping when stem points down.
    """
    items = []
    for i, h in enumerate(noteheads):
        if len(stems[i].inlinks) > 1:
            continue  # skip chords (the stem would go below the notehead)

        # compute some absolute points
        stem_center_y = (stems[i].top + stems[i].bottom) // 2
        notehead_center_x = (h.left + h.right) // 2
        notehead_center_y = (h.top + h.bottom) // 2

        # determine whether to flip the note
        flip = stem_center_y > notehead_center_y

        # place sprites (notehead and stem)
        item = CanvasItem()
        item.add_sprite(Sprite(
            h.left - notehead_center_x,
            h.top - notehead_center_y,
            h.mask
        ))
        item.add_sprite(Sprite(
            stems[i].left - notehead_center_x,
            stems[i].top - notehead_center_y,
            stems[i].mask
        ))

        if flip:
            item = item.flipped()
            item.is_flipped = False  # flip the item, but into the proper orientation

        item.stem_head_y = item.sprites[1].y
        item.stem_head_x = item.sprites[1].x + np.argmax(item.sprites[1].mask[0, :])

        items.append(item)

    return items


def get_quarter_rests(mc: Mashcima):
    return [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "quarter_rest"
    ]


def get_whole_notes(mc: Mashcima):
    empty_noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and not has_outlink_to(mc, o, "ledger_line")
    ]

    return empty_noteheads


def get_half_notes(mc: Mashcima):
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and has_outlink_to(mc, o, "stem")
        and not has_outlink_to(mc, o, "ledger_line")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)


def get_quarter_notes(mc: Mashcima):
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-full"
        and has_outlink_to(mc, o, "stem")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)
