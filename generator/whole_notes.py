from generator.utils import has_outlink_to


def get_whole_notes():
    from generator import CROP_OBJECTS

    empty_noteheads = [
        o for o in CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and not has_outlink_to(o, "ledger_line")
    ]

    # from generator.utils import show_images
    # show_images([e.mask for e in empty_noteheads])

    return empty_noteheads


def get_quarter_rests():
    from generator import CROP_OBJECTS

    rests = [
        o for o in CROP_OBJECTS
        if o.clsname == "quarter_rest"
    ]

    # from generator.utils import show_images
    # show_images([e.mask for e in rests])

    return rests
