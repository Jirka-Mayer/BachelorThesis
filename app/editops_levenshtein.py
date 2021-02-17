from app.vocabulary import VOCABULARY
from typing import List
import Levenshtein


# NOTE: "VOCABULARY" is a list, so the order can be used for encoding
# The encoding is needed since the package only accepts strings, not lists


def _encode_tokens(tokens: List[str]) -> str:
    return "".join([
        chr(VOCABULARY.index(token))
        for token in tokens
    ])


def _decode_tokens(encoded: str) -> List[str]:
    return [
        VOCABULARY[ord(c)]
        for c in encoded
    ]


def _transform_op(op, source_tokens, dest_tokens):
    if op[0] == "insert":
        return ("insert", dest_tokens[op[2]])
    if op[0] == "delete":
        return ("delete", source_tokens[op[1]])
    if op[0] == "replace":
        return ("replace", source_tokens[op[1]], dest_tokens[op[2]])
    raise Exception("Invalid op given")


def editops_levenshtein(gold: str, prediction: str):
    gold_tokens = gold.split()
    prediction_tokens = prediction.split()

    gold_encoded = _encode_tokens(gold_tokens)
    prediction_encoded = _encode_tokens(prediction_tokens)

    # NOTE: editops(source, destination)
    ops = Levenshtein.editops(prediction_encoded, gold_encoded)

    return [_transform_op(o, prediction_tokens, gold_tokens) for o in ops]
