import numpy as np
from typing import Tuple
import random
from generator.GeneratorState import GeneratorState
from generator.printing import *


def fork(label: str, stay_probability: float):
    """Helper for random binary splitting"""
    return random.random() <= stay_probability


def _generate_note_position(state: GeneratorState):
    return random.randint(-5, 5)


def _generate_time_1(state: GeneratorState):
    if fork("Rest or note", 0.3):
        print_quarter_rest(state)
    else:
        print_quarter_note(state, _generate_note_position(state))


def _generate_time_2(state: GeneratorState):
    if fork("Split time in half", 0.7):
        _generate_time_1(state)
        _generate_time_1(state)
    else:
        print_half_note(state, _generate_note_position(state))
        # print_half_rest(state) TODO


def _generate_time_4(state: GeneratorState):
    if fork("Split time in half", 0.8):
        _generate_time_2(state)
        _generate_time_2(state)
    else:
        print_whole_note(state, _generate_note_position(state))
        # print_whole_rest(state) TODO


def generate() -> Tuple[np.ndarray, str]:
    """Generates a pair of image and annotation"""
    state = GeneratorState()

    # generate
    # _generate_time_4(state)  # TODO: currently simplified for bootstrap
    for _ in range(random.choice([1, 2])):
        # print_quarter_note(state, _generate_note_position(state))
        # print_quarter_note(state, random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4]))
        print_quarter_note(state, random.choice([-4, -2, 0, 2, 4]))
        # print_quarter_note(state, random.choice([-4, 4]))
        # _generate_time_1(state)
        
        # if fork("rest or note", 0.5):
        #     print_quarter_note(state, 0)
        # else:
        #     print_quarter_rest(state)

    # crop the result
    img = state.img[:, 0:state.head]

    # clip and flip the result
    img = 1.0 - np.clip(img, 0.0, 1.0)

    # glue the annotation into a string
    annotation = " ".join(state.annotation)

    return img, annotation
