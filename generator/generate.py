import numpy as np
from typing import Tuple, List, Dict
import random


class GeneratorState:
    def __init__(self):
        # generated staff image
        self.img: np.ndarray = None

        # mapping from note position to pixel position
        self.note_positions: Dict[int, int] = {}

        # label for the generated data item
        self.annotation: List[str] = []

        # printer head position in pixels (what has already been printed)
        self.head = 0

        from generator.generate_staff_lines import generate_staff_lines
        self.img, self.note_positions = generate_staff_lines()


def _print_mask(img: np.ndarray, mask: np.ndarray, x: int, y: int):
    img[y:(y + mask.shape[0]), x:(x + mask.shape[1])] += mask


def _print_mask_centered(img: np.ndarray, mask: np.ndarray, x: int, y: int):
    _print_mask(img, mask, x - mask.shape[1] // 2, y - mask.shape[0] // 2)


def _print_quarter_rest(state: GeneratorState):
    from generator import QUARTER_RESTS
    r = random.choice(QUARTER_RESTS)
    space = r.width + random.randint(r.width // 2, r.width * 2)
    _print_mask_centered(
        state.img,
        r.mask,
        state.head + space // 2,
        state.note_positions[0]
    )
    state.annotation.append("qr")
    state.head += space


def _print_whole_note(state: GeneratorState, position: int):
    from generator import WHOLE_NOTES
    n = random.choice(WHOLE_NOTES)
    space = n.width + random.randint(n.width // 2, n.width * 2)
    _print_mask_centered(
        state.img,
        n.mask,
        state.head + space // 2,
        state.note_positions[position]
    )
    state.annotation.append("w" + str(position))
    state.head += space


def _generate_time_4(state: GeneratorState):
    _print_quarter_rest(state)
    _print_quarter_rest(state)
    _print_quarter_rest(state)
    _print_quarter_rest(state)


def generate() -> Tuple[np.ndarray, str]:
    """Generates a pair of image and annotation"""
    state = GeneratorState()

    for i in range(4):
        if random.choice([True, False]):
            _print_whole_note(state, random.randint(-5, 5))
        else:
            _print_quarter_rest(state)

    # _generate_time_4(state)

    # crop the result
    img = state.img[:, 0:state.head]

    # clip and flip the result
    img = 1.0 - np.clip(img, 0.0, 1.0)

    # glue the annotation into a string
    annotation = " ".join(state.annotation)

    # debug
    # print(annotation)
    # import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()

    return img, annotation
