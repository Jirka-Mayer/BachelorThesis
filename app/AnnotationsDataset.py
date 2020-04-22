import numpy as np
from typing import List, Callable
from app.Dataset import Dataset


class AnnotationsDataset(Dataset):
    """
    Contains a list of mashcima annotations
    and lazily generates corresponding images
    """

    def __init__(
            self,
            annotations: List[str],
            generator: Callable[[str], np.ndarray]
    ):
        super().__init__()

        # list of annotations representing the data
        self.annotations = annotations

        # generator that turns annotations to images
        self.generator = generator

    #############
    # Debugging #
    #############

    def check_dataset_visually(self, example_count=10):
        """Shows couple of items in the dataset to visually check the content"""
        import matplotlib.pyplot as plt
        import random

        for _ in range(example_count):
            index = random.randint(0, self.size - 1)
            print(self.get_annotation(index))
            plt.imshow(self.get_image(index))
            plt.show()

    ###########################
    # Internal data interface #
    ###########################

    @property
    def size(self) -> int:
        return len(self.annotations)

    def get_annotation(self, index: int) -> str:
        return self.annotations[index]

    def get_image(self, index: int) -> np.ndarray:
        return self.generator(self.annotations[index])
