import numpy as np
from mashcima.GeneratorState import GeneratorState
from mashcima.utils import show_images
from mashcima.printing import *
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.transform_image import transform_image

"""
Symbols that need be generated:
- rests
    - whole
    - half
    + quarter
    - eight
- simple notes
    + whole
    + half
    + quarter
    - eight
    - sixteenth
- beamed notes
    - eighth
    - sixteenth
- accidentals
    - sharp
    - flat
    - natural
    - staccato dot
    - duration dot
- slurs
- barline
- fermata
- clefs
    - G clef
"""

mc = Mashcima()


def generator():
    global mc
    state = GeneratorState(mc)

    for _ in range(8*4):
        print_quarter_note(state, -4)

    img = state.img[:, 0:state.head]
    img = transform_image(img)
    img = 1.0 - np.clip(img, 0.0, 1.0)
    return img


#show_images([generator() for i in range(5)], row_length=1)
plt.imshow(generator())
plt.show()
