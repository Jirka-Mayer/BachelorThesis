from typing import List, Optional
from app.vocabulary import PITCHES, HIGHEST_PITCH, LOWEST_PITCH
from app.vocabulary import TokenGroup, TimeSignatureTokenGroup, KeySignatureTokenGroup
from app.vocabulary import validate_annotation, stringify_token_groups_to_annotation
from app.vocabulary import is_note, is_barline
import random


def generate_random_annotation() -> str:
    # create items
    count = random.randint(5, 15)
    groups: List[TokenGroup] = []
    i = 0
    while i < count:
        if random.random() < 0.1 and i + 2 < count:
            # beamed group
            beamed_group_length = random.randint(2, min(count - i, 8))
            if random.random() < 0.1:  # boost 2-beams
                beamed_group_length = 2
            groups += _generate_beamed_group(beamed_group_length)
            i += beamed_group_length
        else:
            # simple token
            groups.append(_generate_simple_token_group())
            i += 1

    # add slurs
    in_slur = False
    slur_start = None
    for group in groups:
        if not _is_slurable(group):
            continue
        if not in_slur:
            if random.random() < 0.3:
                in_slur = True
                slur_start = group
        else:
            if random.random() < 0.3:
                slur_start.after_attachments.append("(")
                group.before_attachments = [")"] + group.before_attachments
                in_slur = False

    annotation = stringify_token_groups_to_annotation(groups)

    validate_annotation(annotation)
    return annotation


def _is_slurable(group: TokenGroup) -> bool:
    return is_note(group.token)# or is_barline(group.token)


def _generate_beamed_group(length: int) -> List[TokenGroup]:
    assert length >= 2

    groups = []
    pitches = _generate_beamed_group_pitches(length)
    for i in range(length):
        left_beamed = "=" if i > 0 else ""
        right_beamed = "=" if i < length - 1 else ""
        kind = random.choice(["e", "s", "t"])
        groups.append(_generate_note(
            kind=left_beamed + kind + right_beamed,
            pitch=pitches[i]
        ))

    return groups


def _generate_beamed_group_pitches(length: int) -> List[int]:
    HALF_SPREAD = 4
    center = random.randint(LOWEST_PITCH + HALF_SPREAD, HIGHEST_PITCH - HALF_SPREAD)
    return [center + random.randint(-HALF_SPREAD, HALF_SPREAD) for _ in range(length)]


_SIMPLE_TOKEN_GROUP_CONSTRUCTORS = [
    *(["|"] * 5),
    #"|:",
    #":|",

    lambda: _generate_clef(),
    lambda: _generate_time_signature(),
    lambda: _generate_key_signature(),

    # "lr", "br",
    "wr", "hr", "qr", "er", "sr",
    #"tr",

    *([lambda: _generate_note("w")] * 2),
    *([lambda: _generate_note("h")] * 2),
    *([lambda: _generate_note("q")] * 2),
    *([lambda: _generate_note("e")] * 2),
    *([lambda: _generate_note("s")] * 2),
    #"t{p}",  # thirty-second note
]


def _generate_simple_token_group() -> TokenGroup:
    """Generates notes, rests, clefs, time signature, barlines, key signatures"""
    constructor = random.choice(_SIMPLE_TOKEN_GROUP_CONSTRUCTORS)

    if isinstance(constructor, str):
        return TokenGroup(token=constructor)

    result = constructor()

    if isinstance(result, str):
        return TokenGroup(token=result)

    return result


def _generate_note(kind: str, pitch: Optional[int] = None) -> TokenGroup:
    if pitch is None:
        pitch = str(_generate_random_pitch())
    else:
        pitch = str(pitch)
    accidental = random.choice([
        *([[]] * 10),
        *([["#" + pitch]] * 1),
        *([["b" + pitch]] * 1),
        *([["N" + pitch]] * 1)
    ])
    duration_dots = random.choice([
        *([[]] * 10),
        *([["*"]] * 5),
        *([["**"]] * 1)
    ])
    staccato_dot = random.choice([
        *([[]] * 5),
        *([["."]] * 1)
    ])
    return TokenGroup(
        token=kind + pitch,
        before_attachments=[*accidental],
        after_attachments=[*staccato_dot, *duration_dots]
    )


def _generate_random_pitch() -> int:
    return random.choice(PITCHES)


def _generate_clef() -> str:
    if random.random() < 0.2:
        return "clef.G-2"
    if random.random() < 0.2:
        return "clef.F2"
    if random.random() < 0.2:
        return "clef.C0"
    if random.random() < 0.2:
        return "clef.C2"
    return random.choice([
        "clef.C4", "clef.C-2", "clef.C-4",
        "clef.F0", "clef.F3",
        "clef.G-4",
    ])


def _generate_time_signature() -> TokenGroup:
    if random.random() < 0.3:
        return TokenGroup(token="time.C")
    if random.random() < 0.1:
        return TokenGroup(token="time.C/")
    return TimeSignatureTokenGroup(
        first_number=TokenGroup(token="time." + str(random.randint(0, 9))),
        second_number=TokenGroup(token="time." + str(random.randint(0, 9))),
    )


def _generate_key_signature() -> TokenGroup:
    attachments = []
    for _ in range(random.randint(1, 8)):
        attachments.append(
            random.choice(["#", "b", "N"]) + str(random.randint(-4, 4))
        )

    return KeySignatureTokenGroup(TokenGroup(
        token="NOTHING",
        before_attachments=attachments
    ))
