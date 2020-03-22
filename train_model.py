from mashcima.generate import generate
from app.Network import Network
from app.vocabulary import VOCABULARY
from app.GeneratedDataset import GeneratedDataset


# build the dataset
train_dataset = GeneratedDataset(size=2500, generator=generate)
dev_dataset = GeneratedDataset(size=100, generator=generate)

# train_dataset.check_dataset_visually()
# exit()

# build the network
network = Network(
    continual_saving=False,
    name="Mashcima",
    threads=4,
    num_classes=len(VOCABULARY)
)
network.construct(logdir=Network.create_logdir(network.name))

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=100,
    batch_size=10
)
