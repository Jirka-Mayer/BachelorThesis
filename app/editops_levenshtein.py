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


def editops_levenshtein_sequenced(gold: str, prediction: str):
    """Computes entire sequence-based edit operations, all replacements"""
    # run levenshtein
    gold_tokens = gold.split()
    prediction_tokens = prediction.split()

    gold_encoded = _encode_tokens(gold_tokens)
    prediction_encoded = _encode_tokens(prediction_tokens)

    # NOTE: editops(source, destination)
    ops = Levenshtein.editops(prediction_encoded, gold_encoded)

    # extract all operations that turn prediction to gold (add COPY operations)
    # (COPY, REPLACE, DELETE, INSERT)

    class Op:
        def __init__(self, op_type, pred_from, pred_to, gold_from, gold_to):
            self.op_type = op_type
            self.pred_from = pred_from
            self.pred_to = pred_to
            self.gold_from = gold_from
            self.gold_to =gold_to

        def __repr__(self):
            return f"Op({repr(self.op_type)}, {self.pred_from}, " + \
                f"{self.pred_to}, {self.gold_from}, {self.gold_to})"

    all_operations = []
    prediction_pointer = 0
    gold_pointer = 0
    op_pointer = 0

    def consume_op(op):
        nonlocal prediction_pointer, gold_pointer
        if op[0] == "insert":
            all_operations.append(Op("insert",
                prediction_pointer, prediction_pointer,
                gold_pointer, gold_pointer + 1
            ))
            gold_pointer += 1
        elif op[0] == "delete":
            all_operations.append(Op("delete",
                prediction_pointer, prediction_pointer + 1,
                gold_pointer, gold_pointer
            ))
            prediction_pointer += 1
        elif op[0] == "replace":
            all_operations.append(Op("replace",
                prediction_pointer, prediction_pointer + 1,
                gold_pointer, gold_pointer + 1
            ))
            prediction_pointer += 1
            gold_pointer += 1
        else:
            raise Exception("Unknown op type")

    def attempt_copy():
        nonlocal prediction_pointer, gold_pointer
        assert prediction_tokens[prediction_pointer] == gold_tokens[gold_pointer]
        all_operations.append(Op("copy",
            prediction_pointer, prediction_pointer + 1,
            gold_pointer, gold_pointer + 1
        ))
        prediction_pointer += 1
        gold_pointer += 1

    while op_pointer < len(ops) or \
            prediction_pointer < len(prediction_tokens) or \
            gold_pointer < len(gold_tokens):
        if op_pointer < len(ops):
            op = ops[op_pointer]
            if op[1] == prediction_pointer and op[2] == gold_pointer:
                # the next operation matches
                consume_op(op)
                op_pointer += 1
            else:
                # the next operation does not match
                attempt_copy()
        else:
            # all operations have been consumed
            attempt_copy()

    # all operations should have been consumed and we are at the end
    assert op_pointer == len(ops) \
        and prediction_pointer == len(prediction_tokens) \
        and gold_pointer == len(gold_tokens)

    # get edit sequences
    edit_sequences = []
    sequence_start_index = None  # int when inside a running sequence
    for index, op in enumerate(all_operations):
        # no padding needed as it's already added at the very beginning

        # start a sequence
        if sequence_start_index is None and op.op_type != "copy":
            sequence_start_index = index
            continue
        # end a sequence
        if sequence_start_index is not None and op.op_type == "copy":
            
            # construct the sequence
            from_sequence = [
                prediction_tokens[j] for j in range(
                    all_operations[sequence_start_index].pred_from,
                    all_operations[index - 1].pred_to
                )
            ]
            to_sequence = [
                gold_tokens[j] for j in range(
                    all_operations[sequence_start_index].gold_from,
                    all_operations[index - 1].gold_to
                )
            ]
            edit_sequences.append((from_sequence, to_sequence))
            
            sequence_start_index = None
            continue

    return edit_sequences
