import os
from muscima.io import parse_cropobject_list, CropObject
import itertools
from typing import List, Dict


# where should muscima++ crop objects be loaded from
CROP_OBJECT_DIRECTORY = os.path.join(
    os.environ['HOME'],
    'Data/muscima-pp/v1.0/data/cropobjects_withstaff'
)


class Mashcima:
    def __init__(self, documents: List[str] = None):

        # default documents to load
        if documents is None:
            documents = [
                "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
                "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
                "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
            ]

        ##############################
        # Load and prepare MUSCIMA++ #
        ##############################

        # all loaded crop object documents
        self.DOCUMENTS = [
            parse_cropobject_list(
                os.path.join(CROP_OBJECT_DIRECTORY, doc)
            )
            for doc in documents
        ]

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

        # prevents cyclic imports
        from mashcima.CompositeObject import CompositeObject
        from mashcima.get_symbols import get_whole_notes
        from mashcima.get_symbols import get_quarter_notes
        from mashcima.get_symbols import get_half_notes
        from mashcima.get_symbols import get_quarter_rests
        from mashcima.get_symbols import get_accidentals

        # load all symbols
        # TODO: fix typing - CanvasItem, not CropObject
        self.WHOLE_NOTES: List[CropObject] = get_whole_notes(self)
        self.QUARTER_NOTES: List[CompositeObject] = get_quarter_notes(self)
        self.HALF_NOTES: List[CompositeObject] = get_half_notes(self)
        self.QUARTER_RESTS: List[CropObject] = get_quarter_rests(self)
        self.ACCIDENTALS: List[CropObject] = get_accidentals(self)
