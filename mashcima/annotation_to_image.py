import numpy as np
from app.vocabulary import get_pitch, to_generic
from app.vocabulary import is_after_attachment, is_before_attachment
from app.vocabulary import is_note, is_accidental
from mashcima import Mashcima
from mashcima.Canvas import Canvas
from mashcima.canvas_items.Barline import Barline
from mashcima.canvas_items.Clef import Clef
from mashcima.canvas_items.Rest import Rest
from mashcima.canvas_items.WholeNote import WholeNote
from mashcima.canvas_items.HalfNote import HalfNote
from mashcima.canvas_items.QuarterNote import QuarterNote
from mashcima.canvas_items.FlagNote import FlagNote
from mashcima.canvas_items.BeamedNote import BeamedNote
from mashcima.canvas_items.WholeTimeSignature import WholeTimeSignature
from mashcima.canvas_items.TimeSignature import TimeSignature
from mashcima.canvas_items.KeySignature import KeySignature


ITEM_CONSTRUCTORS = {
    "|": Barline,

    "clef.G": lambda **kwargs: Clef(clef="G", **kwargs),
    "clef.F": lambda **kwargs: Clef(clef="F", **kwargs),
    "clef.C": lambda **kwargs: Clef(clef="C", **kwargs),

    "time.C": lambda **kwargs: WholeTimeSignature(crossed=False, **kwargs),
    "time.C/": lambda **kwargs: WholeTimeSignature(crossed=True, **kwargs),
    # other time signatures are created in a special way

    "w": WholeNote,
    "h": HalfNote,
    "q": QuarterNote,
    "e": lambda **kwargs: FlagNote(flag_kind="e", **kwargs),
    "s": lambda **kwargs: FlagNote(flag_kind="s", **kwargs),

    "wr": lambda **kwargs: Rest(rest_kind="wr", **kwargs),
    "hr": lambda **kwargs: Rest(rest_kind="hr", **kwargs),
    "qr": lambda **kwargs: Rest(rest_kind="qr", **kwargs),
    "er": lambda **kwargs: Rest(rest_kind="er", **kwargs),
    "sr": lambda **kwargs: Rest(rest_kind="sr", **kwargs),

    "e=": lambda **kwargs: BeamedNote(beams=1, left_beamed=False, right_beamed=True, **kwargs),
    "=e=": lambda **kwargs: BeamedNote(beams=1, left_beamed=True, right_beamed=True, **kwargs),
    "=e": lambda **kwargs: BeamedNote(beams=1, left_beamed=True, right_beamed=False, **kwargs),

    "s=": lambda **kwargs: BeamedNote(beams=2, left_beamed=False, right_beamed=True, **kwargs),
    "=s=": lambda **kwargs: BeamedNote(beams=2, left_beamed=True, right_beamed=True, **kwargs),
    "=s": lambda **kwargs: BeamedNote(beams=2, left_beamed=True, right_beamed=False, **kwargs),

    "t=": lambda **kwargs: BeamedNote(beams=3, left_beamed=False, right_beamed=True, **kwargs),
    "=t=": lambda **kwargs: BeamedNote(beams=3, left_beamed=True, right_beamed=True, **kwargs),
    "=t": lambda **kwargs: BeamedNote(beams=3, left_beamed=True, right_beamed=False, **kwargs),
}


def annotation_to_canvas(canvas: Canvas, annotation: str):
    """Appends symbols in annotation to the canvas"""
    before_attachments = []
    after_attachments = []
    item = None

    def _should_key_signature_be_created() -> bool:
        accidentals = [b for b in before_attachments if is_accidental(b)]
        if len(accidentals) == 0:  # no accidentals present
            return False
        if len(accidentals) > 1:
            return True
        if item is None:
            return True
        if not is_note(item):
            return True
        # now we have one accidental in front of a note -> create key signature
        # if this accidental has different pitch than the note
        if get_pitch(accidentals[0]) != get_pitch(item):
            return True
        # otherwise it's just an accidental, no big deal
        return False

    def _create_key_signature():
        accidentals = [b for b in before_attachments if is_accidental(b)]
        types = [to_generic(a) for a in accidentals]
        pitches = [get_pitch(a) for a in accidentals]
        canvas.add(KeySignature(types, pitches))

    def _get_accidental():
        accidentals = [b for b in before_attachments if is_accidental(b)]
        if len(accidentals) == 0:
            return None
        return to_generic(accidentals[0])  # pull out the accidental

    def _get_duration_dots():
        if "*" in after_attachments:
            return "*"
        elif "**" in after_attachments:
            return "**"
        return None

    def _construct_item():
        key_signature_was_created = False
        if _should_key_signature_be_created():
            _create_key_signature()
            key_signature_was_created = True
        canvas.add(ITEM_CONSTRUCTORS[to_generic(item)](**{
            "pitch": get_pitch(item),
            "accidental": _get_accidental() if not key_signature_was_created else None,
            "duration_dots": _get_duration_dots(),
            "staccato": "." in after_attachments,
            "slur_start": "(" in after_attachments,
            "slur_end": ")" in before_attachments,
        }))

    tokens = annotation.split()
    skip_next = False
    for i in range(len(tokens)):
        if skip_next:
            skip_next = False
            continue

        token = tokens[i]
        generic_token = to_generic(token)

        # when we have an item found, we wait for another item or
        # a before attachment to fire the item we have off and start
        # tracking the next item
        if item is not None:
            if is_before_attachment(generic_token) or \
                    not is_after_attachment(generic_token):
                _construct_item()
                before_attachments = []
                after_attachments = []
                item = None

        # handle time signature
        if token.startswith("time."):
            # first create key signature if it has been collected
            if _should_key_signature_be_created():
                _create_key_signature()
                before_attachments = []

            if token in ["time.C", "time.C/"]:
                canvas.add(WholeTimeSignature(crossed=("/" in token)))
                continue
            if (i == len(tokens) - 1) or (not tokens[i + 1].startswith("time.")):
                print("Skipping un-paired time signature:", token)
                continue
            first = int(token[len("time."):])
            second = int(tokens[i + 1][len("time."):])
            canvas.add(TimeSignature(top=first, bottom=second))
            skip_next = True
            continue

        if is_before_attachment(generic_token):
            before_attachments.append(token)
        elif is_after_attachment(generic_token):
            after_attachments.append(token)
        else:
            item = token

    # we ran to the end, now construct the last item
    if item is not None:
        _construct_item()
        before_attachments = []
        after_attachments = []
        item = None

    # there was no last item, but maybe there was a key signature
    if _should_key_signature_be_created():
        _create_key_signature()

    # make sure the canvas produced what it was supposed to produce
    given_annotation = " ".join(annotation.split())
    generated_annotation = " ".join(canvas.get_annotations())
    if given_annotation != generated_annotation:
        print("Canvas generated different annotation from the one given:")
        print("Given: ", given_annotation)
        print("Generated: ", generated_annotation)
        assert given_annotation == generated_annotation  # kill the program


def annotation_to_image(mc: Mashcima, annotation: str) -> np.ndarray:
    """Generates an image from an annotation string"""
    canvas = Canvas()

    annotation_to_canvas(canvas, annotation)

    img = canvas.render(mc)

    return img
