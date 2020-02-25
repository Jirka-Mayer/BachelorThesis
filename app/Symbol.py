import abjad


class Symbol:
    """
    Represents one output of the network
    (network outputs a sequence of these symbols, but also encoded)
    """
    def __init__(self, name):
        # symbol name
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Symbol(%s)" % (self.name,)

    def as_char(self):
        return self.name

        raise Exception("Unknown symbol name: %s" % (self.name,))

    def to_abjad_item(self):
        duration = abjad.Duration(1, 4)

        if self.name == "_":
            return abjad.Rest(duration)
        if self.name == "g'":
            return abjad.Note("g'", duration)
        else:
            return abjad.Note(self.name, duration)

        raise Exception("Unknown symbol name: %s" % (self.name,))
