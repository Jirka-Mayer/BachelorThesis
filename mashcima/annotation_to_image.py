import numpy as np
from typing import List
from mashcima import Mashcima
from mashcima.Canvas import Canvas


def _to_generic(piece: str):
    return piece.rstrip("-0123456789")


def _is_attachment(annotation: str):
    generic = _to_generic(annotation)
    return generic in ["(", ")", "#", "b", "N", ".", "*"]


def _is_note(annotation: str):
    generic = _to_generic(annotation)
    return generic in ["w", "h", "q", "e", "t"]


def _is_simple_item(annotation: str):
    generic = _to_generic(annotation)
    return generic in ["wr", "hr", "qr", "er", "tr"]


def _matches(annotation: str, pattern: str):
    generic = _to_generic(annotation)
    pat = pattern[:-3] if pattern.endswith("{p}") else pattern
    return generic == pat


def _get_pitch(piece: str) -> int:
    generic = piece.rstrip("-0123456789")
    return int(piece[len(generic):])


class Item:
    def __init__(self, annotation: str, index: int):
        self.annotation = annotation
        self.generic_annotation = _to_generic(annotation)
        self.index = index

    def __repr__(self):
        return "Item(" + self.annotation + ")"

    def load_attachments(self, pieces: List[str]):
        # attached symbols before
        i = self.index - 1
        while i >= 0 and _is_attachment(pieces[i]):
            self.handle_attached_symbol_before(pieces[i])
            i -= 1

        # attached symbols after
        i = self.index + 1
        while i < len(pieces) and _is_attachment(pieces[i]):
            self.handle_attached_symbol_before(pieces[i])
            i += 1

    def handle_attached_symbol_before(self, symbol: str):
        pass

    def handle_attached_symbol_after(self, symbol: str):
        pass


class NoteItem(Item):
    def __init__(self, annotation: str, index: int):
        super().__init__(annotation, index)

        self.pitch = _get_pitch(annotation)

        self.accidental = None
        self.slur_end = False
        self.slur_start = False

    def __repr__(self):
        return "NoteItem(accidental=%s, slur_end=%s, slur_start=%s, %s)" % (
            self.accidental,
            self.slur_end,
            self.slur_start,
            self.annotation
        )

    def handle_attached_symbol_before(self, symbol: str):
        for acc in ["#", "b", "N"]:
            if _matches(symbol, acc + "{p}") and _get_pitch(symbol) == self.pitch:
                self.accidental = acc
        if _matches(symbol, ")"):
            self.slur_end = True

    def handle_attached_symbol_after(self, symbol: str):
        if _matches(symbol, "("):
            self.slur_start = True


class Parser:
    def __init__(self, canvas: Canvas, annotation: str):
        # canvas to draw on
        self.canvas = canvas

        # annotation pieces
        self.pieces = annotation.split()

        # individual "canvas" items
        self.items: List[Item] = []

    def run(self):
        for i, p in enumerate(self.pieces):
            if _is_note(p):
                self.items.append(NoteItem(p, i))
            if _is_simple_item(p):
                self.items.append(Item(p, i))

        for i in self.items:
            i.load_attachments(self.pieces)

        print(self.items)
        exit()

        # while len(self.pieces) > 0:
        #     self._parse_symbol()

    def _parse_symbol(self):
        if _matches(self.pieces[0], "w{p}"):
            pitch = _get_pitch(self.pieces[0])
            self.canvas.add_whole_note(pitch=pitch)
            del self.pieces[0]
            return
        if _matches(self.pieces[0], "h{p}"):
            pitch = _get_pitch(self.pieces[0])
            self.canvas.add_half_note(pitch=pitch)
            del self.pieces[0]
            return
        raise Exception("Unknown annotation: " + " ".join(self.pieces))


def annotation_to_canvas(canvas: Canvas, annotation: str):
    """Appends symbols in annotation to the canvas"""
    parser = Parser(canvas, annotation)
    parser.run()


def annotation_to_image(mc: Mashcima, annotation: str) -> np.ndarray:
    """Generates an image from an annotation string"""
    canvas = Canvas(mc)

    annotation_to_canvas(canvas, annotation)

    img = canvas.render()

    # glue the annotations into a string and verify equality
    generated_annotation = " ".join(canvas.get_annotations())
    assert annotation == generated_annotation

    return img
