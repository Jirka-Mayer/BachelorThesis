#!\bin\python3
# Runs whatever is the latest thing being developed

import app
print("==================================\n\n")

# g = app.Generator()
# symbols, staff = g.generate()
# symbols.debug_print()
# import abjad
# abjad.show(staff)
# exit()

# t = app.GeneratedDataset(
#     size=10,
#     name="t",
#     generator_options={},
#     renderer_options={}
# )
# t.generate()
# t.check_dataset_visually(example_count=10)
# exit()


# consider ratio, absolute depends on batch size, I suppose
# 32px -> ~400MB RAM
# 64px -> ~450MB RAM
# 64px deeper channel split -> ~920MB


# setup datasets
train_dataset = app.GeneratedDataset(
    size=50, #250,
    name="train_notes",  # train_chords(1000)
    generator_options={}
)
train_dataset.load_or_generate_and_save()

#train_dataset.check_dataset_visually()
#exit()

dev_dataset = app.GeneratedDataset(
    size=10,
    name="dev_notes",  # dev_chords(50)
    generator_options={}
)
dev_dataset.load_or_generate_and_save()

# setup network
network = app.Network(
    continual_saving=False,
    name="EarlierSplitNetwork",
    threads=4
)
network.construct(logdir=app.Network.create_logdir(network.name))

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=1000,
    batch_size=10
)
