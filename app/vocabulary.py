from typing import List


LOWEST_POSITION = -8  # second additional line below
HIGHEST_POSITION = 8  # second additional line above

# all possible positions
POSITIONS = [str(pos) for pos in reversed(range(LOWEST_POSITION, HIGHEST_POSITION + 1))]

# symbolic vocabulary representation
SYMBOLIC = [
    "|",  # barline
    "|:",  # repeat start
    ":|",  # repeat end
    "fermata",  # fermata above the note

    "clef.C4",
    "clef.C2",
    "clef.C0",  # standard alto clef (middle sitting on position 0 (center line))
    "clef.C-2",
    "clef.C-4",
    "clef.F0",
    "clef.F2",  # standard bass clef (colon sitting on position 2 (line))
    "clef.F3",
    "clef.G-2",  # standard treble clef (curl sitting on position -2 (line))
    "clef.G-4",

    "time.C",  # common (C) meter sign (shorthand for 4/4)
    "time.C/",  # crossed C meter sign (shorthand for 2/2)
    "time.0",
    "time.1",
    "time.2",
    "time.3",
    "time.4",
    "time.5",
    "time.6",
    "time.7",
    "time.8",
    "time.9",

    "#{position}",  # sharp
    "b{position}",  # flat
    "N{position}",  # natural

    "(",  # slur start
    ")",  # slur end
    ".",  # staccato dot
    "*",  # duration dot
    "**",  # duration double dot

    "wr",  # whole rest
    "hr",  # half rest
    "qr",  # quarter rest
    "er",  # eight rest
    "sr",  # sixteenth rest
    "tr",  # thirty-two rest

    "w{position}",  # whole note
    "h{position}",  # half note
    "q{position}",  # quarter note
    "e{position}",  # eight note
    "s{position}",  # sixteenth note
    "t{position}",  # thirty-second note

    "=e{position}",  # beamed left eight note
    "=e={position}",  # beamed both eight note
    "e={position}",  # beamed left eight note

    "=s{position}",  # beamed left sixteenth note
    "=s={position}",  # beamed both sixteenth note
    "s={position}",  # beamed left sixteenth note
]

# build actual vocabulary
VOCABULARY = []
for s in SYMBOLIC:
    if "{position}" in s:
        VOCABULARY += [s.replace("{position}", str(pos)) for pos in POSITIONS]
    else:
        VOCABULARY.append(s)

# check no duplicities
assert len(VOCABULARY) == len(set(VOCABULARY))


def encode_annotation_string(annotation: str) -> List[int]:
    return [VOCABULARY.index(s) for s in annotation.split()]


def decode_annotation_list(annotations: List[int]) -> str:
    return " ".join([VOCABULARY[i] for i in annotations])
