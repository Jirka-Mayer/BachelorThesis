import cv2
import os
import editdistance
from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
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

    # Evaluated metrics:
    # (each builds on the previous removing some nuance)
    #
    # RAW) Raw edit distance
    # GENERATED) Edit distance over generated symbols only
    # SLURLESS) Edit distance without slurs
    # ATTACHMENTLESS) Edit distance without attachments
    # PITCHLESS) Edit distance without attachments and pitches

    total_count = 0
    total_sums = {
        "SER": 0,
        "ITER_RAW": 0,
        "ITER_TRAINED": 0,
        "ITER_SLURLESS": 0,
        "ITER_ORNAMENTLESS": 0,
        "ITER_PITCHLESS": 0,
    }

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

            page_count = 0
            page_sums = {
                "SER": 0,
                "ITER_RAW": 0,
                "ITER_TRAINED": 0,
                "ITER_SLURLESS": 0,
                "ITER_ORNAMENTLESS": 0,
                "ITER_PITCHLESS": 0,
            }

            for i, gold_annotation in enumerate(staves):
                prediction = network.predict(staff_images[i])

                # sort attachments, repair beams and stuff
                repaired_prediction, warnings = repair_annotation(prediction)

                # trim non-important barlines
                repaired_prediction = trim_non_repeat_barlines(repaired_prediction)
                gold_annotation = trim_non_repeat_barlines(gold_annotation)

                # calculate metrics
                item_metrics = _calculate_item_metrics(
                    gold_annotation,
                    repaired_prediction
                )

                # sum metrics
                for metric in total_sums:
                    total_sums[metric] += item_metrics[metric]
                for metric in page_sums:
                    page_sums[metric] += item_metrics[metric]
                total_count += 1
                page_count += 1

                # report on the staff
                print("")
                print("Staff: ", i)
                print("GOLD:       ", gold_annotation)
                print("PREDICTION: ", prediction)
                print("REPAIRED:   ", repaired_prediction)
                print("Warnings:", warnings)

                for metric in item_metrics:
                    print("{:}: {:.2f}".format(metric, item_metrics[metric]))

            # report on the page
            print("")
            print("---------------------------")
            print("Writer: {:02d}      Page: {:03d}".format(writer, page))
            if page_sums == 0:
                print("No metrics recorded")
            else:
                for metric in page_sums:
                    print("{:}: {:.2f}".format(metric, page_sums[metric] / page_count))

    # report on the entire run
    print("\n")
    print("==========================================")
    print("=                Averages                =")
    print("==========================================")
    if total_count == 0:
        print("No metrics recorded")
    else:
        for metric in total_sums:
            print("Average {:}: {:.2f}".format(metric, total_sums[metric] / total_count))


def _calculate_item_metrics(gold: str, prediction: str):
    def _normalized_edit_distance(p: str, g: str, normalize_by: int) -> float:
        ed = editdistance.eval(g.split(), p.split())
        if normalize_by == 0:
            return ed
        return ed / normalize_by

    important_token_count = count_important_tokens(gold)

    return {
        "SER": _normalized_edit_distance(
            prediction,
            gold,
            len(gold.split())
        ),
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
