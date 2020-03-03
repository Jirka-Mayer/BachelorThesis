import numpy as np
import random
import abjad
from typing import List
from app.Label import Label
from app.Channel import Channel


class Generator:
    def __init__(self, length_choices, note_count_choices):
        self.length_choices = length_choices
        self.note_count_choices = note_count_choices

    def generate(self) -> Label:
        """Generates a label"""
        label = Label()

        length = random.choice(self.length_choices)

        for i in range(length):
            channels = self._generate_chord()
            label.append_chord(channels, abjad.Duration(1, 8))

        return label

    def _generate_chord(self) -> List[int]:
        """Generates chord as a list of note channel indices"""
        first_position = Channel.NOTE_CHANNEL_NAMES[0]
        last_position = Channel.NOTE_CHANNEL_NAMES[-1]

        note_count = random.choice(self.note_count_choices)
        note_distances = []
        for i in range(note_count - 1):
            note_distances.append(random.choice([1, 2, 3, 4]))
        size = sum(note_distances)
        total_space = last_position - first_position
        left_space = total_space - size
        position = first_position + random.randint(0, left_space)

        note_positions = np.array([0] + note_distances).cumsum() + position

        return list(note_positions)
