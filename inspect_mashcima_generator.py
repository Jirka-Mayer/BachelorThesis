import numpy as np
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.Canvas import Canvas
import random
from mashcima.generate import *

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
+ ledger lines
- beamed notes
    + eighth
    - sixteenth
+ accidentals
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

for i in range(-8, 8):
    canvas.append(
        random.choice(mc.QUARTER_NOTES),
        i,
        beams_left=random.choice([0, 1, 2]),
        beams_right=random.choice([0, 1, 2]),
        flip=False,
        #accidental=random.choice(mc.ACCIDENTALS),
        #duration_dot=random.choice(mc.DOTS)
    )
canvas.add_slur(canvas.items[2], canvas.items[4])

img = canvas.render()

plt.imshow(img)
plt.show()
