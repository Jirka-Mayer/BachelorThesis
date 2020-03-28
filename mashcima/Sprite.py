import numpy as np


class Sprite:
    def __init__(self, x: int, y: int, mask: np.ndarray):
        # local position within a canvas item
        self.x = x
        self.y = y

        # the actual mask to be printed (image data)
        self.mask = mask

    def flip(self):
        self.x = -self.x - self.mask.shape[1]
        self.y = -self.y - self.mask.shape[0]
        self.mask = np.rot90(np.rot90(self.mask))

    def render(self, img: np.ndarray, parent_x: int, parent_y: int):
        x = self.x + parent_x
        y = self.y + parent_y
        mask = self.mask

        # following code is copied from a helper method and
        # expects: x, y, mask        and renders in canvas pixel space

        y_from = y
        y_to = y + mask.shape[0]
        x_from = x
        x_to = x + mask.shape[1]

        if x_from < 0:
            print("Image does not fit horizontally")
            mask = mask[:, abs(x_from):]
            x_from = 0

        if x_to > img.shape[1]:
            print("Image does not fit horizontally")
            mask = mask[:, :(mask.shape[1] - (x_to - img.shape[1]))]
            x_to = img.shape[1]

        if y_from < 0:
            print("Image does not fit vertically")
            mask = mask[abs(y_from):, :]
            y_from = 0

        if y_to > img.shape[0]:
            print("Image does not fit vertically")
            mask = mask[:(mask.shape[0] - (y_to - img.shape[0])), :]
            y_to = img.shape[0]

        img[y_from:y_to, x_from:x_to] += (1 - img[y_from:y_to, x_from:x_to]) * mask
