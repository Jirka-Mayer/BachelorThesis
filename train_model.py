from mashcima.generate import generate
from app.Network import Network
from app.vocabulary import VOCABULARY
from app.GeneratedDataset import GeneratedDataset
from mashcima import Mashcima


# build the dataset
# train_mc = Mashcima([
#     "CVC-MUSCIMA_W-02_N-06_D-ideal.xml",
#     "CVC-MUSCIMA_W-02_N-13_D-ideal.xml",
#     "CVC-MUSCIMA_W-02_N-17_D-ideal.xml",
# ])
# train_dataset = GeneratedDataset(size=2500, generator=lambda: generate(train_mc))
# dev_mc = Mashcima([
#     "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
# ])
# dev_dataset = GeneratedDataset(size=100, generator=lambda: generate(dev_mc))

# simple datasets for testing logic around training
mc = Mashcima(["CVC-MUSCIMA_W-01_N-10_D-ideal.xml"])
train_dataset = GeneratedDataset(size=2500, generator=lambda: generate(mc))
dev_dataset = GeneratedDataset(size=100, generator=lambda: generate(mc))

# dev_dataset.check_dataset_visually()
# exit()

# build the network
network = Network(
    name="April06",
    num_classes=len(VOCABULARY),
    continual_saving=True,
    create_logdir=True,
    threads=4
)

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
