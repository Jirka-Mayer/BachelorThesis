import argparse
import sys


USAGE_TEXT = '''python experiments/experiment_01.py <command> [<args>]

The available commands are:
   inspect    Inspects datasets that will be used for training and validation
   train      Train new model for the experiment
   test       Test the trained model against annotated muscima parts

Experiment 01:
    - Train on 60K Primus incipits
    - Validate on 4K Primus incipits
    - Generates images with staves above and below
    - Use symbols from all writers except for writers 1 - 5
    - Minimal staff width of 1200px (because Primus incipits are relatively long)

'''


class Experiment01(object):
    def __init__(self):
        parser = argparse.ArgumentParser(usage=USAGE_TEXT)
        parser.add_argument('command', help='Command to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def _prepare_datasets(self):
        from mashcima import Mashcima
        mc = Mashcima(use_cache=True, skip_writers=[1, 2, 3, 4, 5])

        from experiment_utils import prepare_annotations
        training_annotations = prepare_annotations(
            primus_skip=0, primus_take=60000, generated_take=0
        )
        validation_annotations = prepare_annotations(
            primus_skip=60000, primus_take=4000, generated_take=0
        )

        from experiment_utils import prepare_dataset
        training_dataset = prepare_dataset(
            mc, training_annotations, min_staff_with=1200, single_staff=False
        )
        validation_dataset = prepare_dataset(
            mc, validation_annotations, min_staff_with=1200, single_staff=False
        )

        return training_dataset, validation_dataset

    def inspect(self):
        training_dataset, validation_dataset = self._prepare_datasets()

        print("\n\nInspecting TRAINING dataset: (20 items)")
        training_dataset.check_dataset_visually(example_count=20)

        print("\n\nInspecting VALIDATION dataset: (20 items)")
        validation_dataset.check_dataset_visually(example_count=20)

    def train(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', default="experiment_01")
        parser.add_argument('--epochs', default=100, type=int)
        parser.add_argument('--batch_size', default=10, type=int)
        parser.add_argument('--threads', default=4, type=int)
        args = parser.parse_args(sys.argv[2:])

        training_dataset, validation_dataset = self._prepare_datasets()

        # train
        from app.Network import Network
        Network.delete_model(args.model)
        network = Network(
            name=args.model,
            continual_saving=True,
            create_logdir=True,
            threads=args.threads
        )
        network.train(
            training_dataset,
            validation_dataset,
            epochs=args.epochs,
            batch_size=args.batch_size
        )

    def test(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])

        print("Test command is not implemented.")


if __name__ == '__main__':
    Experiment01()
