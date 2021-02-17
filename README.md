# Optical Music Recognition using Deep Neural Networks

## Abstract

Optical music recognition is a challenging field similar in many ways to optical text recognition. It brings, however, many challenges that traditional pipeline-based recognition systems struggle with. The end-to-end approach has proven to be superior in the domain of handwritten text recognition. We tried to apply this approach to the field of OMR. Specifically, we focused on handwritten music recognition. To resolve the lack of training data, we developed an engraving system for handwritten music called Mashcima. This engraving system is successful at mimicking the style of the CVC-MUSCIMA dataset. We evaluated our model on a portion of the CVC-MUSCIMA dataset and the approach seems to be promising.


## Thesis text

You can read the entire thesis at [thesis.pdf](thesis.pdf)


## Setting up on a fresh machine

Make sure you have all the required python packages installed:

    pip install numpy
    pip install cv2
    pip install tensorflow  # tensorflow version 1 is needed
    pip install muscima
    pip install editdistance
    pip install python-Levenshtein
    pip install matplotlib

> Tensorflow has to be in version 1. Project has been tested with versions 1.12.0 and 1.5.0. In case there are some problems, check that the blank symbol of CTC loss is encoded as `num_classes - 1`, not `0`.

Download PRIMUS dataset (as a `.tgz` file) from
[https://grfia.dlsi.ua.es/primus/](https://grfia.dlsi.ua.es/primus/)
It need not be extracted.

Download staff-removal set of CVC-MUSCIMA images from [http://www.cvc.uab.es/cvcmuscima/index_database.html](http://www.cvc.uab.es/cvcmuscima/index_database.html)

Download MUSCIMA++ from [https://ufal.mff.cuni.cz/muscima](https://ufal.mff.cuni.cz/muscima)

Clone the repository.

Copy `config_example.py` to `config.py` and modify accordingly.


## Experiments

The four experiments proposed in the thesis can be found in their respective files `experiment_01.py` up to `experiment_04.py`. To get info on the experiment usage run:

    python3 experiment_01.py --help

Each experiment can be trained, its dataset can be inspected and can be evaluated. Experiments 3 and 4 can be also evaluated on printed PrIMuS incipits.


## Other files

`inspect_annotation_generator.py` when run produces 10 synthetic incipits, prints their Mashcima encoding to the terminal, and displays their engraved image.

`inspect_mashcima_generator.py` contains many inspections that have to be uncommented inside the file. Each inspection allows us to debug one feature of the Mashcima engraving system.

`inspect_mashcima_symbols.py` allows us to inspect symbols that were extracted from the MUSCIMA++ dataset. Inspection to be run has to be uncommented.

`inspect_primus_adapter.py` loads the entire PrIMuS dataset, converts as many insipits to Mashcima encoding as possible, and then validates each incipit conversion by engraving it into an image.

`thesis_images.py` contains code snippets used to generate images for the thesis text.


## Trained models

Trained models are stored inside the folder `trained-models`. One model is contained in a single folder with the model's name (e.g. `experiment_04`). Trained models can be downloaded from a release tag in this Github repository: [https://github.com/Jirka-Mayer/BachelorThesis/releases](https://github.com/Jirka-Mayer/BachelorThesis/releases)

Logs from model training are stored in folder `tf-logs`.
