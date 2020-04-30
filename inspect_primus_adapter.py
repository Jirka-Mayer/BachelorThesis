from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.Canvas import Canvas


def validate_all_loaded_annotations_can_be_rendered():
    primus = load_primus_as_mashcima_annotations(print_warnings=False)
    print("Validating...")
    print("".join(["-" * (len(primus) // 1000)]))
    for i, d in enumerate(primus):
        if i % 1000 == 0:
            print("^", end="", flush=True)
        annotation_to_canvas(Canvas(), d["mashcima"])
    print("")


# MAIN
validate_all_loaded_annotations_can_be_rendered()
