import numpy as np
import random
import pickle
import os
from app.Generator import Generator
from app.SymbolEncoder import SymbolEncoder


class GeneratedDataset:
    def __init__(self, size, name="default", generator_options={}):
        # number of items in the dataset
        self.size = size

        # name of the datased used for saving and loading
        self.name = name

        # height of the normalized image
        self.image_height = 32

        # the data itself
        self.images = None
        self.symbols = None
        self.labels = None  # = encoded symbols

        # generator used for data generation
        self.generator = Generator(**generator_options)

        # encoder used for working with the network output
        self.symbol_encoder = SymbolEncoder()

        # permutation used for data retrieval (when training)
        self.permutation = None

    #############
    # Debugging #
    #############

    def check_dataset_visually(self):
        """Shows couple of items in the dataset to visually check the content"""
        import matplotlib.pyplot as plt

        for i in range(10):
            index = random.randint(0, self.size - 1)
            print("Symbols: %s" % list(map(str, self.symbols[index])))
            print("Label: %s" % self.labels[index])
            plt.imshow(np.dstack([
                self.images[index],
                self.images[index],
                self.images[index]
            ]))
            plt.show()

    ###############
    # Persistence #
    ###############

    def load_or_generate_and_save(self):
        if os.path.isfile(self._path):
            self.load()
        else:
            self.generate()
            self.save()

    def load(self):
        data = pickle.load(open(self._path, "rb"))
        if data["size"] != self.size:
            raise Exception(
                "Saved dataset has size %s, not %s" \
                % (data["size"], self.size)
            )
        self.images = data["images"]
        self.symbols = data["symbols"]
        self.labels = data["labels"]
        print("Dataset '%s' loaded." % (self.name,))

    def save(self):
        pickle.dump({
            "size": self.size,
            "images": self.images,
            "symbols": self.symbols,
            "labels": self.labels
        }, open(self._path, "wb"))
        print("Dataset '%s' saved." % (self.name,))

    @property
    def _path(self):
        """Path, where the dataset should be saved"""
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../generated-datasets/" + self.name + ".pkl"
        )

    ##############
    # Generation #
    ##############

    def generate(self):
        """Generates the entire dataset content
        with parameters specified in the constructor"""
        self.images = []
        self.symbols = []
        self.labels = []
        print("Generating dataset...")
        for i in range(self.size):
            print("%d/%d" % (i+1, self.size))
            image, symbols, label = self._generate_item()
            self.images.append(image)
            self.symbols.append(symbols)
            self.labels.append(label)
        print("Done.")

    def _generate_item(self):
        image, symbols = self.generator.generate()

        # TODO: apply effects to the image here (noise, blur, transform)

        return (
            (image / 255.0),
            symbols,
            self.symbol_encoder.encode_sequence(symbols)
        )

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
        picked_images = []
        picked_labels = []
        for i in indices:
            picked_images.append(self.images[i])
            picked_labels.append(self.labels[i])

        # get maximum image width
        max_image_width = 0
        for i in picked_images:
            if i.shape[1] > max_image_width:
                max_image_width = i.shape[1]

        # create output image tensor and fill it
        image_tensor = np.empty(
            shape=(take, self.image_height, max_image_width),
            dtype=np.float32
        )
        image_widths = np.empty(
            shape=(take,),
            dtype=np.int32
        )

        for i in range(take):
            w = picked_images[i].shape[1]
            image_tensor[i, :, 0:w] = picked_images[i]
            image_tensor[i, :, w:] = 1.0 # pad with white
            image_widths[i] = w

        return image_tensor, picked_labels, image_widths

    def count_batches(self, batch_size):
        """Returns the number of batches, with respect to a given batch size"""
        return len(self.images) // batch_size
