import numpy as np
from typing import Optional, List


class Dataset:
    """
    Abstract class representing a dataset

    Handles the data feeding logic and exposes abstract methods that are used
    as the data source.
    """
    def __init__(self):
        # permutation used for data retrieval (when training)
        self.permutation: Optional[np.ndarray] = None

    ###########################
    # Internal data interface #
    ###########################

    @property
    def size(self) -> int:
        raise NotImplementedError("Override me")

    def get_annotation(self, index: int) -> str:
        raise NotImplementedError("Override me")

    def get_image(self, index: int) -> np.ndarray:
        raise NotImplementedError("Override me")

    ###########################
    # External data interface #
    ###########################

    def prepare_epoch(self):
        """Call this before you start training an epoch"""
        self.permutation = np.random.permutation(self.size)

    def has_batch(self):
        """Returns true if there is at least one more batch to be returned"""
        if self.permutation is None:
            return False
        elif len(self.permutation) == 0:
            return False
        return True

    def next_batch(self, batch_size=1):
        """Returns the next batch for training"""
        # take batch of indices
        take = min(batch_size, len(self.permutation))
        indices = self.permutation[0:take]
        self.permutation = self.permutation[take:]

        # resolve indices to data
        picked_images: List[np.ndarray] = []
        picked_annotations: List[str] = []
        for i in indices:
            picked_images.append(self.get_image(i))
            picked_annotations.append(self.get_annotation(i))

        return picked_images, picked_annotations

    def count_batches(self, batch_size):
        """Returns the number of batches, with respect to a given batch size"""
        return self.size // batch_size
