from app.Network import Network
from app.vocabulary import VOCABULARY
from app.datasets import train_dataset, dev_dataset


# dev_dataset.check_dataset_visually()
# exit()

# build the network
network = Network(
    name="April15",
    num_classes=len(VOCABULARY),
    continual_saving=True,
    create_logdir=True,
    threads=4
)
#network.load()

# train network
network.train(
    train_dataset,
    dev_dataset,
    epochs=100,
    batch_size=10
)

# train and ask
# epoch = 1
# while True:
#     network.train_epoch(train_dataset, dev_dataset, epoch, "?", batch_size=10)
#     if input("continue? [Y/n]") == "n":
#         break
