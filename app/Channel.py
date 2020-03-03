from typing import List
from app.Symbol import Symbol


class Channel:
    """Constants about symbol channels"""

    # names of voice channels
    # VOICE_CHANNEL_NAMES = ["first", "second", "third", "fourth"]
    VOICE_CHANNEL_NAMES = ["first"]

    # symbols that can appear in a voice channel
    VOICE_CHANNEL_SYMBOLS = [
        Symbol.VOICE_NOT_PRESENT,
        Symbol.POS_6_DUR_8,
        Symbol.POS_5_DUR_8,
        Symbol.POS_4_DUR_8,
        Symbol.POS_3_DUR_8,
        Symbol.POS_2_DUR_8,
        Symbol.POS_1_DUR_8,
        Symbol.POS_0_DUR_8,
        Symbol.POS_N1_DUR_8,
        Symbol.POS_N2_DUR_8,
        Symbol.POS_N3_DUR_8,
        Symbol.POS_N4_DUR_8,
        Symbol.POS_N5_DUR_8,
        Symbol.POS_N6_DUR_8,
    ]

    # number symbols in a voice channel
    VOICE_CHANNEL_SYMBOL_COUNT = len(VOICE_CHANNEL_SYMBOLS)

    LOWEST_NOTE_POSITION = -6
    HIGHEST_NOTE_POSITION = 6

    # DEPRECATED NOTE CHANNEL DATA:

    # lists all note channels (their names)
    NOTE_CHANNEL_NAMES = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

    # symbols that can appear in a note channel
    NOTE_CHANNEL_SYMBOLS = [
        Symbol.NO_NOTE,
        Symbol.NOTE_4,
        Symbol.NOTE_8
    ]

    # number of symbols in a note channel
    NOTE_CHANNEL_SYMBOL_COUNT = len(NOTE_CHANNEL_SYMBOLS)

    @staticmethod
    def note_channel_indices_to_pitches(
            indices: List[int],
            clef="treble"
    ) -> List[str]:
        """Converts list of note channel indices to string pitches"""
        return [
            Channel.note_channel_index_to_pitch(index, clef)
            for index in indices
        ]

    @staticmethod
    def note_channel_index_to_pitch(index: int, clef="treble") -> str:
        """Converts index of a note channel to an abjad pitch string"""
        lookup = {
            "treble": {
                6: "a''",
                5: "g''",
                4: "f''",
                3: "e''",
                2: "d''",
                1: "c''",
                0: "b'",
                -1: "a'",
                -2: "g'",
                -3: "f'",
                -4: "e'",
                -5: "d'",
                -6: "c'"
            }
        }
        return lookup[clef][index]
