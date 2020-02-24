import numpy as np
import tensorflow as tf

def sparse_tensor_from_sequences(sequences, dtype=np.int32):
    """Creates a sparse tensor from an array of sequences"""
    indices = []
    values = []

    for n, seq in enumerate(sequences):
        indices.extend(zip([n]*len(seq), range(len(seq))))
        values.extend(seq)

    indices = np.asarray(indices, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray(
        [len(sequences), np.asarray(indices).max(0)[1]+1],
        dtype=np.int64
    )

    return tf.SparseTensorValue(indices, values, shape)
