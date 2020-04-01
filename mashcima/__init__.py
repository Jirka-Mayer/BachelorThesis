import os
from muscima.io import parse_cropobject_list, CropObject
import itertools
from typing import List, Dict
from mashcima.Accidental import Accidental
from mashcima.Sprite import Sprite
from mashcima.CanvasItem import CanvasItem


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

        # load all symbols
        self.WHOLE_NOTES: List[CanvasItem] = get_whole_notes(self)
        self.QUARTER_NOTES: List[CanvasItem] = get_quarter_notes(self)
        self.HALF_NOTES: List[CanvasItem] = get_half_notes(self)
        self.QUARTER_RESTS: List[CanvasItem] = get_quarter_rests(self)
        self.ACCIDENTALS: List[Accidental] = get_accidentals(self)
        self.DOTS: List[Sprite] = get_dots(self)
        self.LEDGER_LINES: List[Sprite] = get_ledger_lines(self)

        print("Mashcima loaded.")
