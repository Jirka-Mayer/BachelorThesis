import cv2
import os
import editdistance
from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
from app.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image
import config
from app.vocabulary import repair_annotation, remove_non_generated_symbols_from_gold_data
from app.vocabulary import remove_attachments_from_annotation, turn_annotation_generic
from app.vocabulary import trim_non_repeat_barlines


def evaluate_model(model_name: str, writers_filter: str, parts_filter: str):
    """Tests a trained model on annotated cvc muscima parts"""
    if writers_filter is None:
        writers_filter = list(range(1, 51))
    else:
        writers_filter = [int(w) for w in writers_filter.split(",")]

    if parts_filter is None:
        parts_filter = list(range(1, 21))
    else:
        parts_filter = [int(w) for w in parts_filter.split(",")]

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

    item_count = 0
    sums = {
        "RAW": 0,
        "GENERATED": 0,
        "SLURLESS": 0,
        "ATTACHMENTLESS": 0,
        "PITCHLESS": 0
    }

    for writer, parts in MUSCIMA_RAW_ANNOTATIONS.items():
        for part, staves in parts.items():

            if writer not in writers_filter:
                continue

            if part not in parts_filter:
                continue

            print("\n")
            print("#############################")
            print("# Writer: {:02d}      Part: {:03d} #".format(writer, part))
            print("#############################")

            image_path = os.path.join(
                config.CVC_MUSCIMA_PATH,
                "w-{:02d}/image/p{:03d}.png".format(writer, part)
            )
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            staff_images = get_staff_images_from_sheet_image(img)
            assert len(staff_images) == len(staves)

            for i, gold_annotation in enumerate(staves):
                prediction = network.predict(staff_images[i])

                # sort attachments, repair beams and stuff
                repaired_prediction, warnings = repair_annotation(prediction)

                # trim non-important barlines
                repaired_prediction = trim_non_repeat_barlines(repaired_prediction)
                gold_annotation = trim_non_repeat_barlines(gold_annotation)

                item_metrics = _calculate_item_metrics(
                    gold_annotation,
                    repaired_prediction
                )

                for metric in sums:
                    sums[metric] += item_metrics[metric]

                item_count += 1

                # report on the staff

                print("")
                print("Staff: ", i)
                print("GOLD:       ", gold_annotation)
                print("PREDICTION: ", prediction)
                print("REPAIRED:   ", repaired_prediction)
                print("Warnings:", warnings)

                for metric in item_metrics:
                    print("{:}: {:.2f}".format(metric, item_metrics[metric]))

    print("\n")
    print("==========================================")
    print("=                Averages                =")
    print("==========================================")
    if item_count == 0:
        print("No metrics recorded")
    else:
        for metric in sums:
            print("Average {:}: {:.2f}".format(metric, sums[metric] / item_count))


def _calculate_item_metrics(gold: str, prediction: str):
    gold_non_generated = remove_non_generated_symbols_from_gold_data(gold)

    def relative_edit_distance(g: str, p: str):
        norm_term = len(g.split())
        if  norm_term == 0:
            print("Skipping edit distance normalization because gold sequence is empty.")
            norm_term = 1
        return editdistance.eval(g.split(), p.split()) / norm_term

    def remove_slurs(annotation: str):
        return " ".join(filter(lambda t: t not in ["(", ")"], annotation.split()))

    return {
        "RAW": relative_edit_distance(
            gold,
            prediction
        ),
        "GENERATED": relative_edit_distance(
            gold_non_generated,
            prediction
        ),
        "SLURLESS": relative_edit_distance(
            remove_slurs(gold_non_generated),
            remove_slurs(prediction)
        ),
        "ATTACHMENTLESS": relative_edit_distance(
            remove_attachments_from_annotation(gold_non_generated),
            remove_attachments_from_annotation(prediction)
        ),
        "PITCHLESS": relative_edit_distance(
            turn_annotation_generic(remove_attachments_from_annotation(gold_non_generated)),
            turn_annotation_generic(remove_attachments_from_annotation(prediction))
        ),
    }
