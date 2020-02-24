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
        return 2

    def encode_sequence(self, symbol_sequence: List[Symbol]):
        return [self.encode(s) for s in symbol_sequence]

    def encode(self, symbol: Symbol):
        if symbol.name == "REST":
            return 0
        if symbol.name == "NOTE":
            return 1

        raise Exception("Unknown symbol name: %s" % (symbol.name,))

    def decode_sequence(self, label_sequence):
        return [self.decode(l) for l in label_sequence]

    def decode(self, label: int):
        if label == 0:
            return Symbol("REST")
        if label == 1:
            return Symbol("NOTE")

        raise Exception("Unknown label: %s" % (label,))
