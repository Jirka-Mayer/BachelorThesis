#!\bin\python3
# Runs whatever is the latest thing being developed

import app
print("==================================\n\n")

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
    name="train_voices",  # train_chords(1000)
    generator_options={}
)
train_dataset.load_or_generate_and_save()

#train_dataset.check_dataset_visually()
#exit()

dev_dataset = app.GeneratedDataset(
    size=10,
    name="dev_voices",  # dev_chords(50)
    generator_options={}
)
dev_dataset.load_or_generate_and_save()

# setup network
network = app.Network(
    continual_saving=False,
    name="VoiceNetwork",
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
