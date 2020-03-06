from generator.utils import has_outlink_to, get_outlink_to
from generator.CompositeObject import CompositeObject


def get_quarter_rests():
    from generator import CROP_OBJECTS
    return [
        o for o in CROP_OBJECTS
        if o.clsname == "quarter_rest"
    ]


def get_whole_notes():
    from generator import CROP_OBJECTS

    empty_noteheads = [
        o for o in CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and not has_outlink_to(o, "ledger_line")
    ]

    return empty_noteheads


def get_half_notes():
    from generator import CROP_OBJECTS

    full_noteheads = [
        o for o in CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and has_outlink_to(o, "stem")
        and not has_outlink_to(o, "ledger_line")
    ]
    stems = [get_outlink_to(o, "stem") for o in full_noteheads]

    composites = []
    for i, h in enumerate(full_noteheads):
        if len(stems[i].inlinks) > 1:
            continue  # skip chords (the stem would go below the notehead)
        stem_center_y = (stems[i].top + stems[i].bottom) // 2
        notehead_center_y = (h.top + h.bottom) // 2
        composites.append(CompositeObject(
            (h.left + h.right) // 2,
            (h.top + h.bottom) // 2,
            [h, stems[i]],
            flip=stem_center_y > notehead_center_y
        ))

    return composites


def get_quarter_notes():
    from generator import CROP_OBJECTS

    full_noteheads = [
        o for o in CROP_OBJECTS
        if o.clsname == "notehead-full"
        and has_outlink_to(o, "stem")
    ]
    stems = [get_outlink_to(o, "stem") for o in full_noteheads]

    composites = []
    for i, h in enumerate(full_noteheads):
        if len(stems[i].inlinks) > 1:
            continue  # skip chords (the stem would go below the notehead)
        stem_center_y = (stems[i].top + stems[i].bottom) // 2
        notehead_center_y = (h.top + h.bottom) // 2
        composites.append(CompositeObject(
            (h.left + h.right) // 2,
            (h.top + h.bottom) // 2,
            [h, stems[i]],
            flip=stem_center_y > notehead_center_y
        ))

    return composites
