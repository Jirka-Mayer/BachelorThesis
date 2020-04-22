from typing import Tuple, Generator
import tarfile
import config

# TODO: HACK
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.Canvas import Canvas


def load_primus_as_mashcima_annotations(take=None):
    print("Loading Primus incipits...")

    ignored_count = 0
    invalid_count = 0

    print("Taking: ", "all" if take is None else take)

    out = []
    for path, primus_annotation in _iterate_tgz_primus(config.PRIMUS_PATH):
        converted = convert_primus_annotation_to_mashcima_annotation(
            primus_annotation
        )
        if converted is None:
            ignored_count += 1
            continue
        if not validate_mashcima_annotation(converted)[0]:
            ignored_count += 1
            invalid_count += 1
            continue

        # TODO: HACK an image has to be creatable from the annotation:
        try:
            annotation_to_canvas(Canvas(), converted)
        except:
            print("Skipping PRIMUS annotation because it's not convertible")
            ignored_count += 1
            continue

        out.append({
            "path": path,
            "primus": primus_annotation,
            "mashcima": converted
        })

        if take is not None and len(out) >= take:
            break

    print("Ignored incipits: ", ignored_count)
    print("Invalid incipits: ", invalid_count)
    print("Loaded incipits: ", len(out))

    return out


def _iterate_tgz_primus(path: str) -> Generator[Tuple[str, str], None, None]:
    with tarfile.open(path, "r:gz") as tar:
        while True:
            item = tar.next()
            if item is None:
                break

            if not str(item.name).endswith(".agnostic"):
                continue

            with tar.extractfile(item) as f:
                yield item.name, f.read().decode("utf-8")


PRIMUS_TO_MASHCIMA_GENERIC_LOOKUP_TABLE = {
    "barline": "|",
    "fermata.above": "fermata",

    "clef.C": "clef.C",
    "clef.F": "clef.F",
    "clef.G": "clef.G",

    "metersign.C": "time.C",
    "metersign.C/": "time.C/",
    "digit.0": "time.0",
    "digit.1": "time.1",
    "digit.2": "time.2",
    "digit.3": "time.3",
    "digit.4": "time.4",
    "digit.5": "time.5",
    "digit.6": "time.6",
    "digit.7": "time.7",
    "digit.8": "time.8",
    "digit.9": "time.9",

    "accidental.sharp": "#",
    "accidental.flat": "b",
    "accidental.natural": "N",

    "slur.start": "(",
    "slur.end": ")",
    "staccato_dot": ".",
    "duration_dot": "*",
    # double dots are joined manually

    "rest.whole": "wr",
    "rest.half": "hr",
    "rest.quarter": "qr",
    "rest.eighth": "er",
    "rest.sixteenth": "sr",
    "rest.thirty_second": "tr",

    "note.whole": "w",
    "note.half": "h",
    "note.quarter": "q",
    "note.eighth": "e",
    "note.sixteenth": "s",
    "note.thirty_second": "t",

    "note.beamedRight1": "e=",
    "note.beamedBoth1": "=e=",
    "note.beamedLeft1": "=e",

    "note.beamedRight2": "s=",
    "note.beamedBoth2": "=s=",
    "note.beamedLeft2": "=s",

    "note.beamedRight3": "t=",
    "note.beamedBoth3": "=t=",
    "note.beamedLeft3": "=t",
}

PRIMUS_TO_MASHCIMA_PITCH_LOOKUP_TABLE = {
    "L7": 8,
    "S6": 7,
    "L6": 6,
    "S5": 5,
    "L5": 4,
    "S4": 3,
    "L4": 2,
    "S3": 1,
    "L3": 0,
    "S2": -1,
    "L2": -2,
    "S1": -3,
    "L1": -4,
    "S0": -5,
    "L0": -6,
    "S-1": -7,
    "L-1": -8,
}

ANNOTATIONS_WITHOUT_PITCH = [
    "barline",
    "fermata.above",

    "metersign.C",
    "metersign.C/",
    "digit.0",
    "digit.1",
    "digit.2",
    "digit.3",
    "digit.4",
    "digit.5",
    "digit.6",
    "digit.7",
    "digit.8",
    "digit.9",

    "slur.start",
    "slur.end",
    "staccato_dot",
    "duration_dot",

    "rest.whole",
    "rest.half",
    "rest.quarter",
    "rest.eighth",
    "rest.sixteenth",
    "rest.thirty_second",
]

IGNORE_INCIPITS_CONTAINING = [
    "multirest",
    "fermata.above",

    "digit.12",
    "digit.11",
    "digit.16",
    "digit.24",

    "rest.thirty_second",  # not present in muscima - we lack the symbols
    "rest.sixty_fourth",
    "rest.quadruple_whole",
    "note.thirty_second",  # not present in muscima - we lack the symbols
    "note.double_whole",
    "note.quadruple_whole",

    "note.beamedRight0",
    "note.beamedLeft0",
    "note.beamedBoth0",

    "note.beamedRight4",
    "note.beamedLeft4",
    "note.beamedBoth4",

    "note.beamedRight5",
    "note.beamedLeft5",
    "note.beamedBoth5",

    "gracenote.double_whole",
    "gracenote.half",
    "gracenote.quarter",
    "gracenote.eighth",
    "gracenote.sixteenth",
    "gracenote.thirty_second",
    "gracenote.beamedRight0",
    "gracenote.beamedRight1",
    "gracenote.beamedBoth1",
    "gracenote.beamedBoth2",
    "gracenote.beamedBoth3",
]

# ignore gracenotes without ignoring the entire incipit
REMOVE_GRACENOTES = True


def convert_primus_annotation_to_mashcima_annotation(primus_annotation: str):
    parts = primus_annotation.split()
    mashcima_annotation = []

    for part_index, part in enumerate(parts):
        i = max(part.rfind("-L"), part.rfind("-S"))
        if i == -1:
            raise Exception("Primus annotation missing pitch: " + part)
        generic = part[:i]
        pitch = part[(i+1):]

        # ---- DOT DISAMBIGUATION BEGIN ----

        # staccato dots (after a note with different pitch)
        if generic == "dot"\
                and parts[part_index - 1].startswith("note.") \
                and not parts[part_index - 1].endswith(pitch):
            generic = "staccato_dot"

        # duration dots (after a note with same pitch)
        if generic == "dot" \
                and parts[part_index - 1].startswith("note.") \
                and parts[part_index - 1].endswith(pitch):
            generic = "duration_dot"

        # duration dots (after a rest)
        elif generic == "dot" and parts[part_index - 1].startswith("rest."):
            generic = "duration_dot"

        # duration double dots (after a dot with same pitch)
        elif generic == "dot" \
                and parts[part_index - 1].startswith("dot") \
                and parts[part_index - 1].endswith(pitch):
            generic = "duration_dot"

        # remove dots following a gracenote
        elif REMOVE_GRACENOTES and generic == "dot" \
                and parts[part_index - 1].startswith("gracenote."):
            continue

        # ---- DOT DISAMBIGUATION END ----

        # skip gracenotes
        if REMOVE_GRACENOTES and generic.startswith("gracenote."):
            continue

        # ignore the incipit if it contains illegal symbols
        if generic in IGNORE_INCIPITS_CONTAINING:
            return None

        if generic not in PRIMUS_TO_MASHCIMA_GENERIC_LOOKUP_TABLE:
            print(parts)
            raise Exception(
                "Primus annotation not convertible: %s (%s)" % (part, generic)
            )

        if pitch not in PRIMUS_TO_MASHCIMA_PITCH_LOOKUP_TABLE:
            # raise Exception("Primus pitch not convertible: " + part)
            return None  # pitch not convertible

        if generic in ANNOTATIONS_WITHOUT_PITCH:
            # convert without pitch
            mashcima_annotation.append(
                PRIMUS_TO_MASHCIMA_GENERIC_LOOKUP_TABLE[generic]
            )
        else:
            # convert with pitch
            mashcima_annotation.append(
                PRIMUS_TO_MASHCIMA_GENERIC_LOOKUP_TABLE[generic] +
                str(PRIMUS_TO_MASHCIMA_PITCH_LOOKUP_TABLE[pitch])
            )

    # join two duration dots into a duration double-dot
    i = 0
    while i < len(mashcima_annotation) - 1:
        if mashcima_annotation[i] == "*" and mashcima_annotation[i + 1] == "*":
            mashcima_annotation[i] = "**"
            del mashcima_annotation[i + 1]
        else:
            i += 1

    return " ".join(mashcima_annotation)


def validate_mashcima_annotation(annotation: str) -> Tuple[bool, str]:
    result, message = mashcima_annotation_has_valid_beams(annotation)
    if not result:
        return result, message
    return True, "everything OK"


def mashcima_annotation_has_valid_beams(annotation: str) -> Tuple[bool, str]:
    tokens = annotation.split()
    in_beam = False
    for t in tokens:

        # skip non-note tokens
        if ("e" not in t) and ("s" not in t) and ("t" not in t):
            continue

        # skip rests -> those are ok
        if t == "er" or t == "sr" or t == "tr":
            continue

        g = t.rstrip("-0123456789")
        s = g.startswith("=")
        e = g.endswith("=")

        if in_beam:
            if not s:
                return False, "Non-finished beam: 'x= x' at: " + t
        else:
            if s:
                return False, "Non-started beam: 'x =x' at: " + t

        in_beam = e

    return True, "everything ok"
