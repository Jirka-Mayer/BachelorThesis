import json
from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
from app.editops_levenshtein import editops_levenshtein_sequenced
from app.vocabulary import repair_annotation
from app.vocabulary import trim_non_repeat_barlines
from app.vocabulary import to_generic
from app.vocabulary import get_pitch
from typing import List


class Statistics:
    JOINER = "  →  "
    EMPTY_SEQUENCE = "∅"

    def __init__(self, title, transformer=None):
        # what to print on the report
        self.title = title
        
        # transforms token sequences before aggregation
        self.transformer = transformer or (lambda x: x)

        # internal statistics "seq": count
        self.stats = {}

    def add_replacements(self, replacements):
        """Adds replacements right from the modified Levenshtein func"""
        for r in replacements:
            self.add_replacement(r[0], r[1])

    def add_replacement(self, pred, gold):
        pred = self.transformer(pred)
        gold = self.transformer(gold)

        if len(pred) == 0:
            pred_str = Statistics.EMPTY_SEQUENCE
        else:
            pred_str = " ".join(pred)

        if len(gold) == 0:
            gold_str = Statistics.EMPTY_SEQUENCE
        else:
            gold_str = " ".join(gold)
        
        key = pred_str + Statistics.JOINER + gold_str

        if key not in self.stats:
            self.stats[key] = 0
        
        self.stats[key] += 1

    def print_report(self):
        print()
        print()
        print("Replacement statistics: " + self.title)
        print("-------------------------------------------------")
        print("<count>: <replacement>")
        for trans, count in sorted(self.stats.items(), key=lambda i: i[1], reverse=True):
            print(str(count).rjust(7) + ": " + trans)


def main():
    print("We are investigating operations required to turn PREDICTION to GOLD")
    print("(it's the inverse of the mistakes the model made)")

    with open("experiment-predictions.json") as f:
        prediction_sheet = json.load(f)

    # TODO: transformer needs to run before levenshtein, not after

    stats = [
        Statistics("Basic stats"),
        Statistics("Generic tokens", lambda seq: [to_generic(t) for t in seq]),
        Statistics("Pitch only", lambda seq: [str(get_pitch(t) or "no") for t in seq]),
    ]

    for writer, parts in MUSCIMA_RAW_ANNOTATIONS.items():
        for part, staves in parts.items():
            for i in range(len(staves)):
                gold = MUSCIMA_RAW_ANNOTATIONS[writer][part][i]
                prediction = prediction_sheet[str(writer)][str(part)][i]

                gold = trim_non_repeat_barlines(repair_annotation(gold)[0])
                prediction = trim_non_repeat_barlines(repair_annotation(prediction)[0])

                for s in stats:
                    replacements = editops_levenshtein_sequenced(
                        s.transformer(gold.split()),
                        s.transformer(prediction.split())
                    )
                    s.add_replacements(replacements)

    for s in stats:
        s.print_report()


main()
