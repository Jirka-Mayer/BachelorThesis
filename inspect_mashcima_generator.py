import numpy as np
from mashcima.GeneratorState import GeneratorState
from mashcima.printing import *
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.transform_image import transform_image
from mashcima.debug import show_images

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
#plt.imshow(generator())
#plt.show()


from mashcima.Canvas import Canvas

canvas = Canvas(mc)
for i in range(-6, 6):
    canvas.append(
        random.choice(mc.QUARTER_NOTES),
        i,
        #beam=random.choice([1, 2]),
        flip=False,
        #accidental=random.choice(mc.ACCIDENTALS),
        #duration_dot=random.choice(mc.DOTS)
    )
canvas.add_slur(canvas.items[2], canvas.items[4])
img = canvas.render()

plt.imshow(img)
plt.show()
