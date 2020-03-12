import numpy as np
import random
from generator.GeneratorState import GeneratorState


####################
# Print primitives #
####################

def print_mask(img: np.ndarray, mask: np.ndarray, x: int, y: int):
    y_from = y
    y_to = y + mask.shape[0]
    x_from = x
    x_to = x + mask.shape[1]

    if x_from < 0:
        print("Image does not fit horizontally")
        mask = mask[:, abs(x_from):]
        x_from = 0

    if x_to > img.shape[1]:
        print("Image does not fit horizontally")
        mask = mask[:, :(mask.shape[1] - (x_to - img.shape[1]))]
        x_to = img.shape[1]

    if y_from < 0:
        print("Image does not fit vertically")
        mask = mask[abs(y_from):, :]
        y_from = 0

    if y_to > img.shape[0]:
        print("Image does not fit vertically")
        mask = mask[:(mask.shape[0] - (y_to - img.shape[0])), :]
        y_to = img.shape[0]

    img[y_from:y_to, x_from:x_to] += mask


def print_mask_centered(img: np.ndarray, mask: np.ndarray, x: int, y: int):
    print_mask(img, mask, x - mask.shape[1] // 2, y - mask.shape[0] // 2)


######################
# Print helper parts #
######################

# TODO: print ledger lines for a note or something


########################
# Print entire symbols #
########################

def print_quarter_rest(state: GeneratorState):
    from generator import QUARTER_RESTS
    r = random.choice(QUARTER_RESTS)
    space = r.width + random.randint(r.width // 2, r.width * 2)
    print_mask_centered(
        state.img,
        r.mask,
        state.head + space // 2,
        state.note_positions[0]
    )
    state.annotation.append("qr")
    state.head += space


def print_whole_note(state: GeneratorState, position: int):
    from generator import WHOLE_NOTES
    n = random.choice(WHOLE_NOTES)
    space = n.width + random.randint(n.width // 2, n.width * 2)
    print_mask_centered(
        state.img,
        n.mask,
        state.head + space // 2,
        state.note_positions[position]
    )
    state.annotation.append("w" + str(position))
    state.head += space


def print_half_note(state: GeneratorState, position: int):
    from generator import HALF_NOTES
    n = random.choice(HALF_NOTES)
    space = n.width + random.randint(n.width // 2, n.width * 2)
    n.print(
        state.img,
        state.head + space // 2,
        state.note_positions[position],
        flip=position >= 0
    )
    state.annotation.append("h" + str(position))
    state.head += space


def print_quarter_note(state: GeneratorState, position: int):
    from generator import QUARTER_NOTES
    # n = random.choice(QUARTER_NOTES)
    n = QUARTER_NOTES[0]
    # space = n.width + random.randint(n.width // 2, n.width * 2)
    space = int(n.width * 5)
    n.print(
        state.img,
        state.head + space // 2,
        state.note_positions[position],
        flip=position >= 0
    )
    state.annotation.append("q" + str(position))
    state.head += space
