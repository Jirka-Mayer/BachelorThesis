from app.Network import Network
from app.GeneratedDataset import GeneratedDataset


class Trainer:
    def __init__(self, network: Network):
        # the neural network being trained
        self._network = network

    def train_all_phases(self):
        self._simple_single_voice()
        self._testing_single_voice()
        # self._introduce_second_voice()

    def _testing_single_voice(self):
        self._train_phase(
            train_size=50,
            dev_size=10,
            phase_name="testing_single_voice",
            generator_options={
                "length_choices": [8, 9, 10, 11, 12, 13, 14, 15, 16],
                "note_count_choices": [1]
            },
            stopping_condition=lambda p: False
        )

    def _simple_single_voice(self):
        self._train_phase(
            train_size=50,
            dev_size=10,
            phase_name="simple_single_voice",
            generator_options={
                "length_choices": [1, 2, 3],
                "note_count_choices": [1]
            },
            stopping_condition=lambda p: p["dev_edit_distance"] < 0.2
        )

    def _introduce_second_voice(self):
        self._train_phase(
            train_size=50,
            dev_size=10,
            phase_name="introduce_second_voice",
            generator_options={
                "length_choices": [1, 2, 3],
                "note_count_choices": [1, 2]
            },
            stopping_condition=lambda p: p["dev_edit_distance"] < 0.05
        )

    def _train_phase(self, train_size, dev_size, phase_name, generator_options, stopping_condition):
        print("=============================")
        print("PHASE:", phase_name)
        print("=============================")
        train_dataset = GeneratedDataset(
            size=train_size,
            name="train_" + str(phase_name),
            generator_options=generator_options
        )
        dev_dataset = GeneratedDataset(
            size=dev_size,
            name="dev_" + str(phase_name),
            generator_options=generator_options
        )
        train_dataset.load_or_generate_and_save()
        dev_dataset.load_or_generate_and_save()
        epoch = 0
        batch_size = 10  # TODO maybe move somewhere
        while True:
            epoch += 1
            loss, edit_distance = self._network.train_epoch(
                train_dataset,
                dev_dataset,
                epoch,
                "?",
                batch_size
            )
            if stopping_condition({
                "epoch": epoch,
                "dev_edit_distance": edit_distance,
                "dev_loss": loss,
            }):
                break
