import numpy as np
import random
import abjad
from typing import List
from app.Label import Label
from app.Channel import Channel


class Generator:
    def __init__(self):
        pass

    def generate(self) -> Label:
        """Generates a label"""
        label = Label()

        length = random.choice([1, 2, 3])

        for i in range(length):
            channels = Generator._generate_chord()
            label.append_chord(channels, abjad.Duration(1, 8))

        return label

    @staticmethod
    def _generate_chord() -> List[int]:
        """Generates chord as a list of note channel indices"""
        first_channel = Channel.NOTE_CHANNEL_NAMES[0]
        last_channel = Channel.NOTE_CHANNEL_NAMES[-1]

        note_count = random.choice([1, 2, 3, 4])
        #note_count = 1  # TODO: DEBUG: no chords, for now
        note_distances = []
        for i in range(note_count - 1):
            note_distances.append(random.choice([1, 2, 3, 4]))
        size = sum(note_distances)
        total_space = last_channel - first_channel
        left_space = total_space - size
        position = first_channel + random.randint(0, left_space)

        note_positions = np.array([0] + note_distances).cumsum() + position

        return note_positions
