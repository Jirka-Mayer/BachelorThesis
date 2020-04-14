from mashcima import Mashcima
from mashcima.Canvas import Canvas
from mashcima.canvas_items.WholeNote import WholeNote
from mashcima.canvas_items.QuarterRest import QuarterRest
from mashcima.canvas_items.HalfNote import HalfNote
from mashcima.canvas_items.QuarterNote import QuarterNote
import matplotlib.pyplot as plt

mc = Mashcima()
canvas = Canvas()

canvas.add(WholeNote(pitch=0))
canvas.add(QuarterRest())
canvas.add(HalfNote(pitch=2, flipped=True))
canvas.add(HalfNote(pitch=-4, flipped=False))
canvas.add(QuarterNote(pitch=2, flipped=True))
canvas.add(QuarterNote(pitch=-4, flipped=False))

print(canvas.get_annotations())

plt.imshow(canvas.render(mc))
plt.show()
