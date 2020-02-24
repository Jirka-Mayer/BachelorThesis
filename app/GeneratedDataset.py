import numpy as np
import random
from app.Generator import Generator
from app.SymbolEncoder import SymbolEncoder


class GeneratedDataset:
    def __init__(self, size, generator_options={}):
        # number of items in the dataset
        self.size = size

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
