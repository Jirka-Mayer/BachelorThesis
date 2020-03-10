from generator.generate import generate
import app
from typing import List
import numpy as np
import cv2
from dataset.vocabulary import decode_annotation_list, encode_annotation_string, VOCABULARY


def normalize_image_height(img):
    target = 64  # TODO: pull constant from config
    ratio = target / img.shape[0]
    w = int(img.shape[1] * ratio)
    return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)


# TODO: build data; extract this class to a file
class Dataset:
    def __init__(self, size: int):
        # height of images
        self.image_height = 64  # TODO: pull constant from config

        # dataset size
        self.size = size

        # the data itself
        self.images: List[np.ndarray] = []
        self.labels: List[List[int]] = []

        # permutation used for data retrieval (when training)
        self.permutation = None

        # generate the data
        for i in range(size):
            img, annotation = generate()
            img = normalize_image_height(img)
            annotation = encode_annotation_string(annotation)
            self.images.append(img)
            self.labels.append(annotation)

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
            shape=(take, self.image_height, max_image_width),
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


# build the dataset
train_dataset = Dataset(2500)
dev_dataset = Dataset(100)

# train_dataset.check_dataset_visually()
# exit()

# build the network
network = app.Network(
    continual_saving=False,
    name="MuscimaSimpleDataNetwork",
    threads=4,
    num_classes=len(VOCABULARY)
)
network.construct(logdir=app.Network.create_logdir(network.name))

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=100,
    batch_size=10
)
