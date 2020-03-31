import numpy as np
from mashcima.utils import has_outlink_to, get_outlink_to
from mashcima.utils import get_connected_components_not_touching_image_border
from mashcima.utils import sort_components_by_proximity_to_point
from mashcima.utils import get_center_of_component
from mashcima import Mashcima
from mashcima.CanvasItem import CanvasItem
from mashcima.Sprite import Sprite
from mashcima.Accidental import Accidental
from typing import List
import cv2


# TODO: some class names so that I can filter in the future:
# (not all though)
#
# ['8th_flag', '8th_rest', 'accent', 'arpeggio_"wobble"', 'beam',
# 'duration-dot', 'dynamics_text', 'f-clef', 'flat', 'g-clef', 'glissando',
# 'grace-notehead-full', 'grace_strikethrough', 'hairpin-cresc.',
# 'hairpin-decr.', 'half_rest', 'instrument_specific', 'key_signature',
# 'ledger_line', 'letter_A', 'letter_P', 'letter_T', 'letter_a', 'letter_c',
# 'letter_d', 'letter_e', 'letter_f', 'letter_g', 'letter_i', 'letter_l',
# 'letter_m', 'letter_n', 'letter_o', 'letter_p', 'letter_r', 'letter_s',
# 'letter_t', 'letter_u', 'measure_separator', 'multi-staff_brace', 'natural',
# 'notehead-empty', 'notehead-full', 'numeral_3', 'numeral_6', 'numeral_7',
# 'other-dot', 'other_text', 'quarter_rest', 'sharp', 'slur', 'staccato-dot',
# 'staff', 'staff_grouping', 'staff_line', 'staff_space', 'stem', 'tempo_text',
# 'thin_barline', 'tie', 'time_signature', 'tuple', 'tuple_bracket/line',
# 'whole-time_mark', 'whole_rest']


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

        item.note_head_sprite = item.sprites[0]
        item.note_stem_sprite = item.sprites[1]

        items.append(item)

    return items


def get_quarter_rests(mc: Mashcima):
    # TODO: convert to CanvasItem
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


def get_accidentals(mc: Mashcima) -> List[Accidental]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["sharp", "flat", "natural"]
    ]
    
    accidentals = []
    for o in crop_objects:
        object_center_x, object_center_y = get_center_of_component(o.mask)

        components = get_connected_components_not_touching_image_border(
            1 - o.mask
        )
        components = sort_components_by_proximity_to_point(
            components,
            object_center_x,
            object_center_y
        )
        if len(components) == 0:
            print(
                "Skipping an accidental, having no components, in document:",
                o.doc
            )
            continue

        component_center_x, component_center_y = get_center_of_component(
            components[0]
        )
        sprite = Sprite(
            -component_center_x,
            -component_center_y,
            o.mask
        )
        a = Accidental(o.clsname, sprite)
        accidentals.append(a)

    # DEBUG: inspect accidentals
    # from mashcima.debug import show_images, draw_cross
    # show_images([
    #     draw_cross(a.sprite.mask, -a.sprite.x, -a.sprite.y, size=5, 1)
    #     for a in accidentals
    # ], 20)
    # exit()

    return accidentals


def get_dots(mc: Mashcima) -> List[Sprite]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["duration-dot", "staccato-dot", "other-dot"]
    ]

    dots = []
    for o in crop_objects:
        object_center_x, object_center_y = get_center_of_component(o.mask)
        dots.append(Sprite(
            -object_center_x,
            -object_center_y,
            o.mask
        ))

    # DEBUG: inspect dots
    # from mashcima.debug import show_images, draw_cross
    # show_images([
    #     draw_cross(d .mask, -d .x, -d .y, size=3, thickness=1)
    #     for d in dots
    # ], 20)
    # exit()

    return dots
