# Dataset generation

Generated data is used via the `GeneratedDataset` class. Typical usage is:


## Basic data generation

```py
dataset = app.GeneratedDataset(
    size=1000,
    name="development"
    generator_options={ ... }
)
dataset.load_or_generate_and_save()
```

You can quickly check what a dataset contains by:

```py
dataset.check_dataset_visually()
```

High-level dataset generation is implemented inside:

```py
dataset.generate()
```

Generation process of a single item is as follows:

1) Generate symbol sequence (the label) `Generator.py`
2) Generate image from the sequence (using lilypond and abjad) `Renderer.py`
3) Apply effects to the image `Effector.py`
4) Normalize the image to target height
  and put it with the label into the dataset


## Feeding data from dataset into the model

TODO
