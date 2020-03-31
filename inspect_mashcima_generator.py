import numpy as np
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.Canvas import Canvas
import random

"""
Symbols that need be generated:
- ledger lines !!!
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
    + sharp
    + flat
    + natural
- dots
    - staccato dot
    - duration dot
- slurs
- barline
- fermata
- clefs
    - G clef
"""

mc = Mashcima()

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
