import numpy as np
from typing import List, Callable, Tuple, Optional
import cv2
from app.vocabulary import decode_annotation_list, encode_annotation_string
from app.Network import Network


def normalize_image_height(img: np.ndarray):
    target = Network.IMAGE_HEIGHT
    ratio = target / img.shape[0]
    w = int(img.shape[1] * ratio)
    return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)


class GeneratedDataset:
    """
    Acts as the glue between a mashcima and the network.
    Is only a container for generated data.
    Also performs image height normalization and label encoding.
    """

    def __init__(
            self,
            images: List[np.ndarray] = None,
            annotations: List[str] = None,
            size: Optional[int] = None,
            generator: Optional[Callable[[], Tuple[np.ndarray, str]]] = None
    ):
        if images is None:
            images = []
        if annotations is None:
            annotations = []

        # dataset size
        assert len(images) == len(annotations)
        self.size = len(images)

        # the data itself
        self.images: List[np.ndarray] = [normalize_image_height(img) for img in images]
        self.labels: List[List[int]] = [encode_annotation_string(a) for a in annotations]

        # permutation used for data retrieval (when training)
        self.permutation = None

        # generate the data
        if size is not None:
            while len(self.images) < size:
                img, annotation = generator()
                img = normalize_image_height(img)
                annotation = encode_annotation_string(annotation)
                self.images.append(img)
                self.labels.append(annotation)
                self.size += 1

    #############
    # Debugging #
    #############

    def check_dataset_visually(self, example_count=10):
        """Shows couple of items in the dataset to visually check the content"""
        import matplotlib.pyplot as plt
        import random

        for _ in range(example_count):
            index = random.randint(0, self.size - 1)
            print(decode_annotation_list(self.labels[index]))
            # plt.imshow(np.dstack([
            #     self.images[index],
            #     self.images[index],
            #     self.images[index]
            # ]))
            plt.imshow(self.images[index])
            plt.show()

    ##################
    # Data interface #
    ##################

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
        picked_labels: List[List[int]] = []
        for i in indices:
            picked_images.append(self.images[i])
            picked_labels.append(self.labels[i])

        # get maximum image width
        max_image_width = max([i.shape[1] for i in picked_images])

        # create output image tensor and fill it
        image_tensor = np.empty(
            shape=(take, Network.IMAGE_HEIGHT, max_image_width),
            dtype=np.float32
        )
        image_widths = np.empty(shape=(take,), dtype=np.int32)

        for i in range(take):
            w = picked_images[i].shape[1]
            image_tensor[i, :, 0:w] = picked_images[i]
            image_tensor[i, :, w:] = 1.0  # pad with white
            image_widths[i] = w

        return image_tensor, picked_labels, image_widths

    def count_batches(self, batch_size):
        """Returns the number of batches, with respect to a given batch size"""
        return len(self.images) // batch_size
