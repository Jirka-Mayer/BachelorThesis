#!\bin\python3
# Runs whatever is the latest thing being developed

import app


# setup datasets
train_dataset = app.GeneratedDataset(
    size=8,
    name="train",
    generator_options={}
)
train_dataset.load_or_generate_and_save()

dev_dataset = app.GeneratedDataset(
    size=2,
    name="dev",
    generator_options={}
)
dev_dataset.load_or_generate_and_save()

# setup network
network = app.Network(
    continual_saving=False,
    name="TestingNetwork",
    threads=1
)
network.construct(logdir="tf-logs")

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=1,
    batch_size=1
)
