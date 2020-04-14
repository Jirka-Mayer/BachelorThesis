import numpy as np
from mashcima.utils import has_outlink_to, get_outlink_to
from mashcima.utils import get_connected_components_not_touching_image_border
from mashcima.utils import sort_components_by_proximity_to_point
from mashcima.utils import get_center_of_component
from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
from typing import List, Tuple, Dict


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
    canvas items. Handles flipping when stem points down.
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
        item = SpriteGroup()
        item.add("notehead", Sprite(
            h.left - notehead_center_x,
            h.top - notehead_center_y,
            h.mask
        ))
        item.add("stem", Sprite(
            stems[i].left - notehead_center_x,
            stems[i].top - notehead_center_y,
            stems[i].mask
        ))

        if flip:
            item = item.create_flipped_copy()

        stem_sprite = item.sprite("stem")
        item.add_point("stem_head", (
            stem_sprite.x + np.argmax(stem_sprite.mask[0, :]),
            stem_sprite.y
        ))

        items.append(item)

    return items


def get_quarter_rests(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "quarter_rest"
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("rest", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask
        ))
        items.append(item)

    return items


def get_whole_notes(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and not has_outlink_to(mc, o, "ledger_line")
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("notehead", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask
        ))
        items.append(item)

    return items


def get_half_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and has_outlink_to(mc, o, "stem")
        and not has_outlink_to(mc, o, "ledger_line")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)


def get_quarter_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-full"
        and has_outlink_to(mc, o, "stem")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)


def get_accidentals(mc: Mashcima) -> Tuple[List[Sprite], List[Sprite], List[Sprite]]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["sharp", "flat", "natural"]
    ]

    sharps = []
    flats = []
    naturals = []
    
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
        if o.clsname == "sharp":
            sharps.append(sprite)
        elif o.clsname == "flat":
            flats.append(sprite)
        elif o.clsname == "natural":
            naturals.append(sprite)

    return sharps, flats, naturals


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

    return dots


def get_ledger_lines(mc: Mashcima) -> List[Sprite]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["ledger_line"]
    ]

    lines = []
    for o in crop_objects:
        object_center_x, object_center_y = get_center_of_component(o.mask)
        lines.append(Sprite(
            -object_center_x,
            -object_center_y,
            o.mask
        ))

    return lines


def get_bar_lines(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["thin_barline"]
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("barline", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask,
            print_render_warnings=(False if o.height > 350 else True)
        ))
        items.append(item)

    return items


def get_g_clefs(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["g-clef"]
    ]

    items = []
    for o in crop_objects:
        staff = get_outlink_to(mc, o, "staff")
        staff_line = None
        line = 0
        for l in staff.outlinks:
            resolved_link = mc.CROP_OBJECT_LOOKUP_DICTS[o.doc][l]
            if resolved_link.clsname == "staff_line":
                if line == 3:  # counted from top, from zero
                    staff_line = resolved_link
                    break
                line += 1

        item = SpriteGroup()
        item.add("clef", Sprite(
            -o.width // 2,
            o.top - staff_line.top,  # sitting on the G line
            o.mask
        ))
        items.append(item)

    return items


def get_f_clefs(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["f-clef"]
    ]

    items = []
    for o in crop_objects:
        staff = get_outlink_to(mc, o, "staff")
        staff_line = None
        line = 0
        for l in staff.outlinks:
            resolved_link = mc.CROP_OBJECT_LOOKUP_DICTS[o.doc][l]
            if resolved_link.clsname == "staff_line":
                if line == 1:  # counted from top, from zero
                    staff_line = resolved_link
                    break
                line += 1

        item = SpriteGroup()
        item.add("clef", Sprite(
            -o.width // 2,
            o.top - staff_line.top,  # sitting on the F line
            o.mask
        ))
        items.append(item)

    return items


def get_c_clefs(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["c-clef"]
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("clef", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask
        ))
        items.append(item)

    return items


def get_time_marks(mc: Mashcima) -> Dict[str, List[SpriteGroup]]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["time_signature"]
    ]

    KEY_MAP = {
        "numeral_0": "time_0",
        "numeral_1": "time_1",
        "numeral_2": "time_2",
        "numeral_3": "time_3",
        "numeral_4": "time_4",
        "numeral_5": "time_5",
        "numeral_6": "time_6",
        "numeral_7": "time_7",
        "numeral_8": "time_8",
        "numeral_9": "time_9",
        "whole-time_mark": "time_c",
    }

    items = {
        "time_0": [],
        "time_1": [],
        "time_2": [],
        "time_3": [],
        "time_4": [],
        "time_5": [],
        "time_6": [],
        "time_7": [],
        "time_8": [],
        "time_9": [],
        "time_c": [],
    }

    for o in crop_objects:
        for l in o.outlinks:
            outlink = mc.CROP_OBJECT_LOOKUP_DICTS[o.doc][l]
            if outlink.clsname == "staff":
                continue
            item = SpriteGroup()
            item.add("symbol", Sprite(
                -outlink.width // 2,
                -outlink.height // 2,
                outlink.mask
            ))
            items[KEY_MAP[outlink.clsname]].append(item)

    return items
