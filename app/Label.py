import abjad
from typing import List, Dict, Set
from app.Symbol import Symbol
from app.Channel import Channel


class Label:
    """
    Represents the symbol stream (in all channels) that the network outputs.
    (not yet encoded to integers, see the SymbolEncoder for that)
    """
    def __init__(self):
        # individual symbol channels
        self._channels: Dict[any, List[Symbol]] = {}
        Label._create_empty_channels(self)

        # the abjad staff, representing the label
        # (used for image rendering)
        self._staff = abjad.Staff()

    @staticmethod
    def _create_empty_channels(self):
        """Creates empty channels on a label instance"""
        for name in Channel.NOTE_CHANNEL_NAMES:
            self._channels[name] = []

    def get_channel(self, name):
        """Returns value of a channel"""
        return self._channels[name]

    def set_channel(self, name, value: List[Symbol]):
        """Sets value of a channel"""
        self._channels[name] = value

    #########
    # Debug #
    #########

    def debug_print(self):
        """Prints the stream into the console for debugging"""
        indices = list(Channel.NOTE_CHANNEL_NAMES)
        indices.reverse()
        for i in indices:
            text = str(i).rjust(3) + " : "
            for symbol in self._channels[i]:
                text += symbol.short.ljust(2)
            print(text)
        print()

    ##################
    # Label creation #
    ##################

    def append_chord(self, note_channels: List[int], duration: abjad.Duration):
        """Appends a single chord to the staff"""
        # append to abjad
        abjad_chord = abjad.Chord(
            Channel.note_channel_indices_to_pitches(
                note_channels,
                clef="treble"
            ),
            duration
        )
        self._staff.append(abjad_chord)

        # append symbols in note channels
        note_symbol = Symbol.note_symbol_from_duration(duration)
        for name in Channel.NOTE_CHANNEL_NAMES:
            if name in note_channels:
                self._channels[name].append(note_symbol)
            else:
                self._channels[name].append(Symbol.NO_NOTE)

