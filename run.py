#!\bin\python3
# Runs whatever is the latest thing being developed

import app
import matplotlib.pyplot as plt


dataset = app.GeneratedDataset(
    size=3,
    generator_options={}
)
dataset.generate()
dataset.check_dataset_visually()
