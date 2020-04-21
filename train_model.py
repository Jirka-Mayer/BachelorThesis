from app.Network import Network
from app.datasets import train_dataset, dev_dataset
import config


# dev_dataset.check_dataset_visually()
# exit()

# build the network
network = Network(
    name=config.MODEL_NAME,
    continual_saving=True,
    create_logdir=True,
    threads=config.NUM_THREADS
)
# network = Network.load(
#     name=config.MODEL_NAME,
#     continual_saving=True,
#     create_logdir=True,
#     threads=config.NUM_THREADS
# )

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
