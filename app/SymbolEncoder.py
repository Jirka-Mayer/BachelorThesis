from typing import List
from app.Symbol import Symbol


class SymbolEncoder:
    """
    Encodes/decodes symbols into the vector/scalar form,
    that the network outputs
    """
    def __init__(self):
        pass

    def encode_sequence(self, symbol_sequence: List[Symbol]):
        return [self.encode(s) for s in symbol_sequence]

    def encode(self, symbol: Symbol):
        if symbol.name == "NOTE":
            return 1
        if symbol.name == "REST":
            return 2

        raise Error("Unknown symbol name: " + symbol.name)
