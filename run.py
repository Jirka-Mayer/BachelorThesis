#!\bin\python3
# Runs whatever is the latest thing being developed

import app
import matplotlib.pyplot as plt

generator = app.Generator()
img = generator.generate_notation_row_image(
    crop_row=0,
    normalize_image_height=True
)

plt.imshow(img)
plt.show()
