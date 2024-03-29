import argparse
import sys


USAGE_TEXT = '''python experiment_04.py <command> [<args>]

The available commands are:
   inspect             Inspects datasets that will be used for training and validation
   train               Train new model for the experiment
   evaluate            Evaluate the trained model against annotated muscima parts
   evaluate_on_primus  Evaluate trained model against some primus incipits
   evaluate_on_real    Evaluate trained model against real scanned sheet music

Experiment 04:
    - Train on 63K Primus incipits and 63K generated incipits
    - Validate on 1K Primus incipits
    - Generates images with staves above and below
    - Use symbols from all writers except for the evaluating ones
    - Minimal staff width of 1200px

'''


class Experiment04(object):
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
        mc = Mashcima(use_cache=True, skip_writers=[13, 17, 20, 34, 41, 49])

        from experiment_utils import prepare_annotations
        training_annotations = prepare_annotations(
            primus_skip=0, primus_take=63127, generated_take=63127
        )
        validation_annotations = prepare_annotations(
            primus_skip=63127, primus_take=1000, generated_take=0
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
        parser.add_argument('--model', default="experiment_04")
        parser.add_argument('--epochs', default=10, type=int)
        parser.add_argument('--batch_size', default=10, type=int)
        parser.add_argument('--threads', default=4, type=int)
        parser.add_argument('--load_model', action="store_true", help="continue training a model")
        parser.add_argument('--seed_offset', default=0, type=int)
        args = parser.parse_args(sys.argv[2:])

        # set seed
        import tensorflow as tf
        import numpy as np
        import random
        tf.set_random_seed(20200524 + args.seed_offset)
        np.random.seed(20200524 + args.seed_offset)
        random.seed(20200524 + args.seed_offset)

        training_dataset, validation_dataset = self._prepare_datasets()

        # train
        from app.Network import Network

        # continue training
        if args.load_model:
            # load old one
            print("Loading old model...")
            network = Network.load(args.model)
        else:
            # delete old one
            if Network.exists(args.model):
                if input("Type 'yes' to delete the old, trained model.") != "yes":
                    exit("No model will be overwritten")
                print("Deleting old model...")
                Network.delete_model(args.model)

            # create new one
            print("Creating new model...")
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

    def evaluate(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', default="experiment_04")
        parser.add_argument('--writers', type=str, help="writers to evaluate on e.g. '1,2,3'")
        parser.add_argument('--pages', type=str, help="pages to evaluate on e.g. '1,2,3'")
        args = parser.parse_args(sys.argv[2:])

        from experiment_evaluation import evaluate_model
        evaluate_model(args.model, args.writers, args.pages)

    def evaluate_on_real(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', default="experiment_04")
        args = parser.parse_args(sys.argv[2:])

        from experiment_evaluation import evaluate_on_real
        evaluate_on_real(args.model)

    def evaluate_on_primus(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', default="experiment_04")
        args = parser.parse_args(sys.argv[2:])

        from experiment_evaluation import evaluate_on_primus
        evaluate_on_primus(args.model)


if __name__ == '__main__':
    Experiment04()
