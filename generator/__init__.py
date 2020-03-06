import os
from muscima.io import parse_cropobject_list, CropObject
import itertools
from typing import List
from generator.whole_notes import get_whole_notes, get_quarter_rests


##############################
# Load and prepare MUSCIMA++ #
##############################

# where should muscima++ crop objects be loaded from
CROP_OBJECT_DIRECTORY = os.path.join(
    os.environ['HOME'],
    'Data/muscima-pp/v1.0/data/cropobjects_withstaff'
)

# all loaded crop object documents
DOCUMENTS = [
    parse_cropobject_list(
        os.path.join(CROP_OBJECT_DIRECTORY, "CVC-MUSCIMA_W-01_N-19_D-ideal.xml")
    )
]

# all loaded crop objects
CROP_OBJECTS = list(itertools.chain(*DOCUMENTS))

# dictionary of loaded crop objects
CROP_OBJECT_DICT = {c.objid: c for c in CROP_OBJECTS}


####################################
# Prepare all symbols for printing #
####################################

# load all symbols
WHOLE_NOTES: List[CropObject] = get_whole_notes()
QUARTER_RESTS: List[CropObject] = get_quarter_rests()
