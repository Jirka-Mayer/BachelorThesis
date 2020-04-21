import os

# name of the model that will be used in training and validation
MODEL_NAME = "unnamed"

# how many threads to use for training and inference
NUM_THREADS = 1

# path to the primus dataset as downloaded from:
# https://grfia.dlsi.ua.es/primus/
PRIMUS_PATH = os.path.expanduser(
    '~/Data/primusCalvoRizoAppliedSciences2018.tgz'
)

# path to the cvc-muscima ideal images directory, downloaded from:
# http://www.cvc.uab.es/cvcmuscima/index_database.html
CVC_MUSCIMA_PATH = os.path.expanduser(
    '~/Data/cvc-muscima/ideal'
)

# where should muscima++ crop objects be loaded from
# https://ufal.mff.cuni.cz/muscima
MUSCIMA_PP_CROP_OBJECT_DIRECTORY = os.path.expanduser(
    '~/Data/muscima-pp/v1.0/data/cropobjects_withstaff'
)
