import os
from muscima.io import parse_cropobject_list, CropObject
import itertools
from typing import List, Dict
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
import cv2


# where should muscima++ crop objects be loaded from
CROP_OBJECT_DIRECTORY = os.path.join(
    os.environ['HOME'],
    'Data/muscima-pp/v1.0/data/cropobjects_withstaff'
)


class Mashcima:
    def __init__(self, documents: List[str] = None):
        print("Loading mashcima...")

        # default documents to load
        if documents is None:
            documents = [
                "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
                "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
                "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
            ]

        # TODO: HACK: load all documents
        # TODO: this will be the default in the future
        # documents = [
        #     os.path.join(CROP_OBJECT_DIRECTORY, f)
        #     for f in os.listdir(CROP_OBJECT_DIRECTORY)
        # ]

        ##############################
        # Load and prepare MUSCIMA++ #
        ##############################

        # all loaded crop object documents
        self.DOCUMENTS = []
        for i, doc in enumerate(documents):
            print("Parsing document %d/%d ..." % (i + 1, len(documents)))
            self.DOCUMENTS.append(
                parse_cropobject_list(
                    os.path.join(CROP_OBJECT_DIRECTORY, doc)
                )
            )

        # names of the documents
        # (used for resolving document index from document name)
        self.DOCUMENT_NAMES = [doc[0].doc for doc in self.DOCUMENTS]

        # all loaded crop objects in one list
        self.CROP_OBJECTS = list(itertools.chain(*self.DOCUMENTS))

        # for each document name create an objid lookup dictionary
        # (to make resolving outlinks easier)
        self.CROP_OBJECT_LOOKUP_DICTS: Dict[str, Dict[int, CropObject]] = {
            self.DOCUMENT_NAMES[i]: {c.objid: c for c in doc}
            for i, doc in enumerate(self.DOCUMENTS)
        }

        ####################################
        # Prepare all symbols for printing #
        ####################################

        print("Preparing symbols...")

        # prevents cyclic imports
        from mashcima.get_symbols import get_whole_notes
        from mashcima.get_symbols import get_quarter_notes
        from mashcima.get_symbols import get_half_notes
        from mashcima.get_symbols import get_quarter_rests
        from mashcima.get_symbols import get_accidentals
        from mashcima.get_symbols import get_dots
        from mashcima.get_symbols import get_ledger_lines
        from mashcima.get_symbols import get_bar_lines
        from mashcima.get_symbols import get_g_clefs
        from mashcima.get_symbols import get_f_clefs
        from mashcima.get_symbols import get_c_clefs

        # load all symbols
        self.WHOLE_NOTES: List[SpriteGroup] = get_whole_notes(self)
        self.QUARTER_NOTES: List[SpriteGroup] = get_quarter_notes(self)
        self.HALF_NOTES: List[SpriteGroup] = get_half_notes(self)
        self.QUARTER_RESTS: List[SpriteGroup] = get_quarter_rests(self)
        self.FLATS: List[Sprite] = []
        self.SHARPS: List[Sprite] = []
        self.NATURALS: List[Sprite] = []
        self.FLATS, self.SHARPS, self.NATURALS = get_accidentals(self)
        self.DOTS: List[Sprite] = get_dots(self)
        self.LEDGER_LINES: List[Sprite] = get_ledger_lines(self)
        self.BAR_LINES: List[SpriteGroup] = get_bar_lines(self)
        self.G_CLEFS: List[SpriteGroup] = get_g_clefs(self)
        self.F_CLEFS: List[SpriteGroup] = get_f_clefs(self)
        self.C_CLEFS: List[SpriteGroup] = get_c_clefs(self)

        # load default symbols if needed
        if len(self.F_CLEFS) == 0:
            self.F_CLEFS.append(SpriteGroup().add("clef", _load_default_sprite("clef_f")))
        if len(self.G_CLEFS) == 0:
            self.G_CLEFS.append(SpriteGroup().add("clef", _load_default_sprite("clef_g")))
        if len(self.C_CLEFS) == 0:
            self.C_CLEFS.append(SpriteGroup().add("clef", _load_default_sprite("clef_c")))

        # validate there is no empty list
        assert len(self.WHOLE_NOTES) > 0
        assert len(self.QUARTER_NOTES) > 0
        assert len(self.HALF_NOTES) > 0
        assert len(self.QUARTER_RESTS) > 0
        assert len(self.FLATS) > 0
        assert len(self.SHARPS) > 0
        assert len(self.NATURALS) > 0
        assert len(self.DOTS) > 0
        assert len(self.LEDGER_LINES) > 0
        assert len(self.BAR_LINES) > 0
        assert len(self.G_CLEFS) > 0
        assert len(self.F_CLEFS) > 0
        assert len(self.C_CLEFS) > 0

        print("Mashcima loaded.")


def _load_default_sprite(name: str) -> Sprite:
    print("Loading default sprite:", name)
    dir = os.path.join(os.path.dirname(__file__), "default_symbols")
    img_path = os.path.join(dir, name + ".png")
    center_path = os.path.join(dir, name + ".txt")
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) / 255
    x = -img.shape[1] // 2
    y = -img.shape[0] // 2
    if os.path.isfile(center_path):
        with open(center_path) as f:
            x, y = tuple(f.readline().split())
            x = -int(x)
            y = -int(y)
    return Sprite(x, y, img)
