#!\bin\python3
# Runs whatever is the latest thing being developed

import app

t = app.GeneratedDataset(
    size=10,
    name="t",
    generator_options={},
    renderer_options={}
)
t.generate()
t.check_dataset_visually(example_count=10)
exit()


# TODO: put this into some utilities
def create_logdir(model_name):
    import os
    import datetime
    if not os.path.exists("tf-logs"):
        os.mkdir("tf-logs")
    return "tf-logs/{}-{}".format(
        model_name,
        datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    )

# setup datasets
train_dataset = app.GeneratedDataset(
    size=50, #250,
    name="train",
    generator_options={}
)
train_dataset.load_or_generate_and_save()

# train_dataset.check_dataset_visually()
# exit()

dev_dataset = app.GeneratedDataset(
    size=10,
    name="dev",
    generator_options={}
)
dev_dataset.load_or_generate_and_save()

# setup network
network = app.Network(
    continual_saving=False,
    name="TestingNetwork",
    threads=4
)
network.construct(logdir=create_logdir(network.name))

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=100,
    batch_size=10
)
