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

    @staticmethod
    def note_symbol_from_duration(duration: abjad.Duration):
        lookup = {
            "4": Symbol.NOTE_4,
            "8": Symbol.NOTE_8,
        }
        return lookup[duration.lilypond_duration_string]
