from mashcima.Sprite import Sprite


ANNOTATION_LOOKUP = {
    "sharp": "#",
    "flat": "b",
    "natural": "N"
}


class Accidental:
    def __init__(self, accidental_type: str, sprite: Sprite):
        # type of the accidental
        # TODO: double sharp, double flat
        self.accidental_type = accidental_type
        assert accidental_type in ["sharp", "flat", "natural"]

        # the sprite to render
        self.sprite = sprite

        self.annotation = ANNOTATION_LOOKUP[self.accidental_type]
