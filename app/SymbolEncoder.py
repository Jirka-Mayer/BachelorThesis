from typing import List
from app.Symbol import Symbol


class SymbolEncoder:
    """
    Encodes/decodes symbols into the vector/scalar form,
    that the network outputs
    """
    def __init__(self):
        pass

    @property
    def num_classes(self):
        """Returns number of output classes"""
        return 6

    def encode_sequence(self, symbol_sequence: List[Symbol]):
        return [self.encode(s) for s in symbol_sequence]

    def encode(self, symbol: Symbol):
        if symbol.name == "_":
            return 0
        if symbol.name == "g'":
            return 1
        if symbol.name == "c'":
            return 2
        if symbol.name == "b'":
            return 3
        if symbol.name == "e''":
            return 4
        if symbol.name == "g''":
            return 5

        raise Exception("Unknown symbol name: %s" % (symbol.name,))

    def decode_sequence(self, label_sequence):
        return [self.decode(l) for l in label_sequence]

    def decode(self, label: int):
        if label == 0:
            return Symbol("_")
        if label == 1:
            return Symbol("g'")
        if label == 2:
            return Symbol("c'")
        if label == 3:
            return Symbol("b'")
        if label == 4:
            return Symbol("e''")
        if label == 5:
            return Symbol("g''")

        raise Exception("Unknown label: %s" % (label,))
