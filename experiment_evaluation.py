import cv2
import os
import editdistance
from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
from app.real_annotations import REAL_RAW_ANNOTATIONS
from app.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image
import config
from app.vocabulary import repair_annotation
from app.vocabulary import trim_non_repeat_barlines
from app.vocabulary import count_important_tokens
from app.vocabulary import iter_raw_transformation
from app.vocabulary import iter_trained_transformation
from app.vocabulary import iter_slurless_transformation
from app.vocabulary import iter_ornamentless_transformation
from app.vocabulary import iter_pitchless_transformation
from app.editops_levenshtein import editops_levenshtein


def evaluate_model(model_name: str, writers_filter: str, pages_filter: str):
    """Tests a trained model on annotated cvc muscima pages"""
    if writers_filter is None:
        writers_filter = list(range(1, 51))
    else:
        writers_filter = [int(w) for w in writers_filter.split(",")]

    if pages_filter is None:
        pages_filter = list(range(1, 21))
    else:
        pages_filter = [int(w) for w in pages_filter.split(",")]

    from app.Network import Network
    network = Network.load(model_name)

    print("\n")

    total_metric_aggregate = _initialize_metrics_aggregate()

    for writer, pages in MUSCIMA_RAW_ANNOTATIONS.items():
        for page, staves in pages.items():

            if writer not in writers_filter:
                continue

            if page not in pages_filter:
                continue

            print("\n")
            print("#############################")
            print("# Writer: {:02d}      Page: {:03d} #".format(writer, page))
            print("#############################")

            image_path = os.path.join(
                config.CVC_MUSCIMA_PATH,
                "w-{:02d}/image/p{:03d}.png".format(writer, page)
            )
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            staff_images = get_staff_images_from_sheet_image(img)
            assert len(staff_images) == len(staves)

            page_metric_aggregate = _initialize_metrics_aggregate()

            for i, gold_annotation in enumerate(staves):
                prediction = network.predict(staff_images[i])

                PERFORM_REPAIR = True

                if PERFORM_REPAIR:
                    # sort attachments, repair beams and stuff
                    repaired_prediction, warnings = repair_annotation(prediction)

                    # trim non-important barlines
                    repaired_prediction = trim_non_repeat_barlines(repaired_prediction)
                    gold_annotation = trim_non_repeat_barlines(gold_annotation)
                else:
                    repaired_prediction = prediction
                    warnings = []

                # calculate metrics
                staff_metrics = _calculate_staff_metrics(
                    gold_annotation,
                    repaired_prediction
                )

                # sum metrics
                _add_metrics(page_metric_aggregate, staff_metrics)
                _add_metrics(total_metric_aggregate, staff_metrics)

                # report on the staff
                print("")
                print("Staff: ", i)
                print("GOLD:       ", gold_annotation)
                print("PREDICTION: ", prediction)
                print("REPAIRED:   ", repaired_prediction)
                print("Warnings:", warnings)
                print("****")
                _report_staff_metrics(staff_metrics)

            # report on the page
            print("")
            print("---------------------------")
            print("Writer: {:02d}      Page: {:03d}".format(writer, page))
            _report_page_metrics(page_metric_aggregate)

    # report on the entire run
    print("\n")
    print("==========================================")
    print("=                Averages                =")
    print("==========================================")
    _report_dataset_metrics(total_metric_aggregate)


def evaluate_on_real(model_name: str):
    """Evaluates a model on real scanned music pages"""
    from app.Network import Network
    network = Network.load(model_name)

    print("\n")

    total_metric_aggregate = _initialize_metrics_aggregate()

    for file, staves in REAL_RAW_ANNOTATIONS.items():
        print("\n")
        print("##########################")
        print("# File: " + file)
        print("##########################")

        image_path = os.path.join(
            os.path.dirname(__file__),
            "real-images/" + file
        )
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # pre-processing to bring it closer looking to the cvc muscima dataset
        img = 255 - img
        _, img = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)

        # split staves (use dilation!)
        staff_images = get_staff_images_from_sheet_image(img, dilate=True)
        assert len(staff_images) == len(staves)

        page_metric_aggregate = _initialize_metrics_aggregate()

        for i, gold_annotation in enumerate(staves):
            # skip "None" annotated staves
            if gold_annotation is None:
                continue

            prediction = network.predict(staff_images[i])

            PERFORM_REPAIR = True

            if PERFORM_REPAIR:
                # sort attachments, repair beams and stuff
                repaired_prediction, warnings = repair_annotation(prediction)

                # trim non-important barlines
                repaired_prediction = trim_non_repeat_barlines(repaired_prediction)
                gold_annotation = trim_non_repeat_barlines(gold_annotation)
            else:
                repaired_prediction = prediction
                warnings = []

            # calculate metrics
            staff_metrics = _calculate_staff_metrics(
                gold_annotation,
                repaired_prediction
            )

            # sum metrics
            _add_metrics(page_metric_aggregate, staff_metrics)
            _add_metrics(total_metric_aggregate, staff_metrics)

            # report on the staff
            print("")
            print("Staff: ", i)
            print("GOLD:       ", gold_annotation)
            print("PREDICTION: ", prediction)
            print("REPAIRED:   ", repaired_prediction)
            print("Warnings:", warnings)
            print("****")
            _report_staff_metrics(staff_metrics)

        # report on the file
        print("")
        print("---------------------------")
        print("File: " + file)
        _report_page_metrics(page_metric_aggregate)

        # report on the entire run

    print("\n")
    print("==========================================")
    print("=                Averages                =")
    print("==========================================")
    _report_dataset_metrics(total_metric_aggregate)


def evaluate_on_primus(model_name: str, take_last=100):
    """Test model on printed primus incipits"""
    from mashcima.primus_adapter import load_primus_as_mashcima_annotations
    import tarfile
    from config import PRIMUS_PATH
    import numpy as np
    import matplotlib.pyplot as plt

    print("EVALUATING ON THE LAST " + str(take_last) + " PRIMUS INCIPITS")

    # load evaluation data
    primus = load_primus_as_mashcima_annotations()
    primus = primus[-take_last:]  # take the last n incipits

    print("Loading primus images...")
    with tarfile.open(PRIMUS_PATH, "r:gz") as tar:
        for incipit in primus:
            member = tar.getmember(
                incipit["path"].replace(".agnostic", ".png")
            )
            with tar.extractfile(member) as f:
                img = cv2.imdecode(
                    np.asarray(bytearray(f.read()), dtype=np.uint8),
                    cv2.IMREAD_GRAYSCALE
                )
                img = 255 - img  # flip
                img = img / img.max()  # normalize
                # zoom out by 1.5
                zoomed = np.zeros(shape=(int(img.shape[0] * 1.5), img.shape[1]), dtype=np.float32)
                top = int(img.shape[0] * 0.25)
                zoomed[top:top+img.shape[0], :] = img
                incipit["img"] = zoomed  # save

    # perform the evaluation
    from app.Network import Network
    network = Network.load(model_name)

    total_metric_aggregate = _initialize_metrics_aggregate()

    for incipit in primus:
        gold_annotation = incipit["mashcima"]
        prediction = network.predict(incipit["img"])

        # sort attachments, repair beams and stuff
        repaired_prediction, warnings = repair_annotation(prediction)

        # trim non-important barlines
        repaired_prediction = trim_non_repeat_barlines(repaired_prediction)
        gold_annotation = trim_non_repeat_barlines(gold_annotation)

        # calculate metrics
        staff_metrics = _calculate_staff_metrics(
            gold_annotation,
            repaired_prediction
        )

        # sum metrics
        _add_metrics(total_metric_aggregate, staff_metrics)

        # report on the staff
        print("")
        print("Staff: ", incipit["path"])
        print("GOLD:       ", gold_annotation)
        print("PREDICTION: ", prediction)
        print("REPAIRED:   ", repaired_prediction)
        print("Warnings:", warnings)
        print("****")
        _report_staff_metrics(staff_metrics)

        # show the incipit image
        # plt.imshow(incipit["img"])
        # plt.show()

    # report on the entire run
    print("\n")
    print("==========================================")
    print("=                Averages                =")
    print("==========================================")
    _report_dataset_metrics(total_metric_aggregate)


#######################################################
# Private functions implementing various helper logic #
#######################################################


def _initialize_metrics_aggregate():
    return {
        "STAFF_COUNT": 0,
        "SER": 0,
        "EDITS": [],
        "EDIT_COUNT": 0,
        "GOLD_TOKEN_COUNT": 0,
        "ITER_RAW": 0,
        "ITER_TRAINED": 0,
        "ITER_SLURLESS": 0,
        "ITER_ORNAMENTLESS": 0,
        "ITER_PITCHLESS": 0,
    }


def _add_metrics(metrics_aggregate, metrics):
    for metric in metrics_aggregate:
        metrics_aggregate[metric] += metrics[metric]


def _report_staff_metrics(metrics):
    m = metrics

    print("SER: {:.4f}".format(m["SER"]))

    print("EDITS:", m["EDITS"])
    print("EDIT_COUNT:", m["EDIT_COUNT"])
    print("GOLD_TOKEN_COUNT:", m["GOLD_TOKEN_COUNT"])

    print("ITER_RAW: {:.4f}".format(m["ITER_RAW"]))
    print("ITER_TRAINED: {:.4f}".format(m["ITER_TRAINED"]))
    print("ITER_SLURLESS: {:.4f}".format(m["ITER_SLURLESS"]))
    print("ITER_ORNAMENTLESS: {:.4f}".format(m["ITER_ORNAMENTLESS"]))
    print("ITER_PITCHLESS: {:.4f}".format(m["ITER_PITCHLESS"]))


def _report_page_metrics(metrics_aggregate):
    m = metrics_aggregate

    c = m["STAFF_COUNT"]

    if c == 0:
        print("No metrics recorded")
        return

    print("total STAFF_COUNT:", c)

    print("avg SER: {:.4f}".format(m["SER"] / c))

    #print("total EDITS:", m["EDITS"]) # a long list - don't print
    print("total EDIT_COUNT:", m["EDIT_COUNT"])
    print("total GOLD_TOKEN_COUNT:", m["GOLD_TOKEN_COUNT"])

    print("avg ITER_RAW: {:.4f}".format(m["ITER_RAW"] / c))
    print("avg ITER_TRAINED: {:.4f}".format(m["ITER_TRAINED"] / c))
    print("avg ITER_SLURLESS: {:.4f}".format(m["ITER_SLURLESS"] / c))
    print("avg ITER_ORNAMENTLESS: {:.4f}".format(m["ITER_ORNAMENTLESS"] / c))
    print("avg ITER_PITCHLESS: {:.4f}".format(m["ITER_PITCHLESS"] / c))

    ser = m["EDIT_COUNT"] / m["GOLD_TOKEN_COUNT"]
    print("total norm SER: {:.4f}".format(ser))


def _report_dataset_metrics(metrics_aggregate):
    _report_page_metrics(metrics_aggregate)

    # TODO: aggregate edits and do a frequency analysis
    print("TODO: edits frequency analysis")


def _calculate_staff_metrics(gold: str, prediction: str):
    def _normalized_edit_distance(p: str, g: str, normalize_by: int) -> float:
        ed = editdistance.eval(g.split(), p.split())
        if normalize_by == 0:
            return ed
        return ed / normalize_by

    important_token_count = count_important_tokens(gold)

    edits = editops_levenshtein(gold, prediction)
    edit_count = editdistance.eval(gold.split(), prediction.split())

    # "edits" look like this:
    # [("insert", "#4"), ("delete", "b8"), ("replace", (what) ".", (with) "*")]

    # make sure both edit distance libraries agree
    assert len(edits) == edit_count

    return {
        "STAFF_COUNT": 1,  # increment staff count by one

        "SER": _normalized_edit_distance(
            prediction,
            gold,
            len(gold.split())
        ),
        
        "EDITS": edits,
        "EDIT_COUNT": len(edits),
        "GOLD_TOKEN_COUNT": len(gold.split()),

        "ITER_RAW": _normalized_edit_distance(
            iter_raw_transformation(prediction),
            iter_raw_transformation(gold),
            important_token_count
        ),
        "ITER_TRAINED": _normalized_edit_distance(
            iter_trained_transformation(prediction),
            iter_trained_transformation(gold),
            important_token_count
        ),
        "ITER_SLURLESS": _normalized_edit_distance(
            iter_slurless_transformation(prediction),
            iter_slurless_transformation(gold),
            important_token_count
        ),
        "ITER_ORNAMENTLESS": _normalized_edit_distance(
            iter_ornamentless_transformation(prediction),
            iter_ornamentless_transformation(gold),
            important_token_count
        ),
        "ITER_PITCHLESS": _normalized_edit_distance(
            iter_pitchless_transformation(prediction),
            iter_pitchless_transformation(gold),
            important_token_count
        ),
    }
