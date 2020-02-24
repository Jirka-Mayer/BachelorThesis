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
        return "S-" + self.name

    def __repr__(self):
        return "Symbol(%s)" % (self.name,)

    def to_abjad_item(self):
        duration = abjad.Duration(1, 4)

        if self.name == "NOTE":
            return abjad.Note("g'", duration)
        if self.name == "REST":
            return abjad.Rest(duration)

        raise Exception("Unknown symbol name: %s" % (self.name,))
