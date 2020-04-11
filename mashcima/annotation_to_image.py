import numpy as np
from typing import List
from mashcima import Mashcima
from mashcima.Canvas import Canvas


def _to_generic(annotation: str):
    return annotation.rstrip("-0123456789")


def _is_attachment(annotation: str):
    generic = _to_generic(annotation)
    return generic in ["(", ")", "#", "b", "N", ".", "*"]


def _is_note(annotation: str):
    generic = _to_generic(annotation)
    return generic in [
        "w", "h", "q", "e", "s", "t",
        "=e", "=e=", "e=",
        "=s", "=s=", "s=",
        "=t", "=t=", "t=",
    ]


def _is_simple_item(annotation: str):
    generic = _to_generic(annotation)
    return generic in [
        "|",
        "wr", "hr", "qr", "er", "sr", "tr"
    ]


def _matches(annotation: str, pattern: str):
    generic = _to_generic(annotation)
    pat = pattern[:-3] if pattern.endswith("{p}") else pattern
    return generic == pat


def _get_pitch(annotation: str) -> int:
    generic = annotation.rstrip("-0123456789")
    return int(annotation[len(generic):])


class Item:
    def __init__(self, annotation: str, index: int):
        self.annotation = annotation
        self.generic_annotation = _to_generic(annotation)
        self.index = index

        self.slur_end = False
        self.slur_start = False

    def __repr__(self):
        return "Item(" + self.annotation + ")"

    def load_attachments(self, tokens: List[str]):
        # attached symbols before
        i = self.index - 1
        while i >= 0 and _is_attachment(tokens[i]):
            self.handle_attached_symbol_before(tokens[i])
            i -= 1

        # attached symbols after
        i = self.index + 1
        while i < len(tokens) and _is_attachment(tokens[i]):
            self.handle_attached_symbol_after(tokens[i])
            i += 1

    def handle_attached_symbol_before(self, symbol: str):
        if _matches(symbol, ")"):
            self.slur_end = True

    def handle_attached_symbol_after(self, symbol: str):
        if _matches(symbol, "("):
            self.slur_start = True

    def print_to_canvas(self, canvas: Canvas):
        if self.generic_annotation == "|":
            canvas.add_bar_line(
                slur_start=self.slur_start,
                slur_end=self.slur_end
            )
        elif self.generic_annotation == "qr":
            canvas.add_quarter_rest()
        elif self.generic_annotation == "sr":
            canvas.add_quarter_rest()
            print("TODO: print sr instead of qr")
        else:
            raise Exception("Cannot print to canvas: " + self.annotation)


class NoteItem(Item):
    def __init__(self, annotation: str, index: int):
        super().__init__(annotation, index)

        self.pitch = _get_pitch(annotation)

        self.accidental = None

    def __repr__(self):
        return "NoteItem(accidental=%s, slur_end=%s, slur_start=%s, %s)" % (
            self.accidental,
            self.slur_end,
            self.slur_start,
            self.annotation
        )

    def handle_attached_symbol_before(self, symbol: str):
        super().handle_attached_symbol_before(symbol)
        for acc in ["#", "b", "N"]:
            if _matches(symbol, acc + "{p}") and _get_pitch(symbol) == self.pitch:
                self.accidental = acc

    def handle_attached_symbol_after(self, symbol: str):
        super().handle_attached_symbol_after(symbol)

    def print_to_canvas(self, canvas: Canvas):
        if self.generic_annotation == "w":
            canvas.add_whole_note(pitch=self.pitch, accidental=self.accidental)
        elif self.generic_annotation == "h":
            canvas.add_half_note(pitch=self.pitch, accidental=self.accidental)
        elif self.generic_annotation == "q":
            canvas.add_quarter_note(
                pitch=self.pitch,
                accidental=self.accidental,
                slur_start=self.slur_start,
                slur_end=self.slur_end
            )
        elif self.generic_annotation in ["e=", "=e", "=e="]:
            canvas.add_quarter_note(
                pitch=self.pitch,
                accidental=self.accidental,
                slur_start=self.slur_start,
                slur_end=self.slur_end
            )
            print("TODO: implement beamed notes")
        elif self.generic_annotation in ["s=", "=s", "=s="]:
            canvas.add_quarter_note(pitch=self.pitch, accidental=self.accidental)
            print("TODO: implement beamed notes")
        else:
            raise Exception("Cannot print to canvas: " + self.annotation)


class Parser:
    def __init__(self, canvas: Canvas, annotation: str):
        # canvas to draw on
        self.canvas = canvas

        # annotation tokens
        self.annotation = annotation
        self.tokens = annotation.split()

        # individual "canvas" items
        self.items: List[Item] = []

    def run(self):
        """Main method that appends items to canvas based on the annotation"""
        for i, p in enumerate(self.tokens):
            if _is_note(p):
                self.items.append(NoteItem(p, i))
            if _is_simple_item(p):
                self.items.append(Item(p, i))

        for i in self.items:
            i.load_attachments(self.tokens)

        print(self.annotation)

        print(self.items)

        for i in self.items:
            i.print_to_canvas(self.canvas)


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
