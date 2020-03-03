import abjad


class SymbolInstance:  # private, should not leak outside this file
    """
    Represents an output class that can be produced by the network
    on one of it's output channels.
    """

    def __init__(self, name, short):
        # symbol name
        self.name = name

        # short representation (for debug)
        self.short = short

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Symbol(%s)" % (self.name,)


class Symbol(SymbolInstance):  # public (like an interface)

    # symbols for a note channel
    NOTE_4 = SymbolInstance("NOTE_4", "4")  # present quarter note in a chord
    NOTE_8 = SymbolInstance("NOTE_8", "8")  # present eight note in a chord
    NO_NOTE = SymbolInstance("NO_NOTE", "-")  # missing note in a chord

    # symbols for a voice channel
    VOICE_NOT_PRESENT = SymbolInstance("VOICE_NOT_PRESENT", "-")
    POS_6_DUR_8 = SymbolInstance("POS_6_DUR_8", "6$8")
    POS_5_DUR_8 = SymbolInstance("POS_5_DUR_8", "5$8")
    POS_4_DUR_8 = SymbolInstance("POS_4_DUR_8", "4$8")
    POS_3_DUR_8 = SymbolInstance("POS_3_DUR_8", "3$8")
    POS_2_DUR_8 = SymbolInstance("POS_2_DUR_8", "2$8")
    POS_1_DUR_8 = SymbolInstance("POS_1_DUR_8", "1$8")
    POS_0_DUR_8 = SymbolInstance("POS_0_DUR_8", "0$8")
    POS_N1_DUR_8 = SymbolInstance("POS_N1_DUR_8", "N1$8")
    POS_N2_DUR_8 = SymbolInstance("POS_N2_DUR_8", "N2$8")
    POS_N3_DUR_8 = SymbolInstance("POS_N3_DUR_8", "N3$8")
    POS_N4_DUR_8 = SymbolInstance("POS_N4_DUR_8", "N4$8")
    POS_N5_DUR_8 = SymbolInstance("POS_N5_DUR_8", "N5$8")
    POS_N6_DUR_8 = SymbolInstance("POS_N6_DUR_8", "N6$8")

    @staticmethod
    def note_symbol_from_duration(duration: abjad.Duration):
        lookup = {
            "4": Symbol.NOTE_4,
            "8": Symbol.NOTE_8,
        }
        return lookup[duration.lilypond_duration_string]

    @staticmethod
    def voice_symbol_from_position_and_duration(
            position: int,
            duration: abjad.Duration
    ):
        lookup = {
            "8": {
                6: Symbol.POS_6_DUR_8,
                5: Symbol.POS_5_DUR_8,
                4: Symbol.POS_4_DUR_8,
                3: Symbol.POS_3_DUR_8,
                2: Symbol.POS_2_DUR_8,
                1: Symbol.POS_1_DUR_8,
                0: Symbol.POS_0_DUR_8,
                -1: Symbol.POS_N1_DUR_8,
                -2: Symbol.POS_N2_DUR_8,
                -3: Symbol.POS_N3_DUR_8,
                -4: Symbol.POS_N4_DUR_8,
                -5: Symbol.POS_N5_DUR_8,
                -6: Symbol.POS_N6_DUR_8,
            },
        }
        return lookup[duration.lilypond_duration_string][position]
