import numpy as np
from typing import List
from muscima.io import CropObject
from generator.printing import print_mask


class CompositeObject:
    """Composite of multiple crop objects that has
    a center point and can be printed"""
    def __init__(self, x: int, y: int, objects: List[CropObject], flip: bool):
        # list of crop objects that are part of this composite object
        self._objects = objects

        # helper dimensions (relative to source image)
        self._left = min([o.left for o in objects])
        self._right = max([o.right for o in objects])
        self._top = min([o.top for o in objects])
        self._bottom = max([o.bottom for o in objects])

        # dimensions
        self.width = self._right - self._left
        self.height = self._bottom - self._top

        # center of this object, that is specified when printing
        # and around which rotation is based
        # (relative to this object's mask)
        self.x = x - self._left
        self.y = y - self._top

        # compute the composite mask
        self.mask = np.zeros(shape=(self.height, self.width), dtype=np.float32)
        for o in self._objects:
            print_mask(
                self.mask, o.mask,
                o.left - self._left,
                o.top - self._top
            )
        self.mask[self.mask > 0] = 1

        # flip if requested
        if flip:
            self.mask = np.rot90(np.rot90(self.mask))
            self.x = self.width - self.x
            self.y = self.height - self.y

    def print(self, img: np.ndarray, x: int, y: int, flip=False):
        print_mask(
            img,
            np.rot90(np.rot90(self.mask)) if flip else self.mask,
            x - (self.width - self.x if flip else self.x),
            y - (self.height - self.y if flip else self.y)
        )
