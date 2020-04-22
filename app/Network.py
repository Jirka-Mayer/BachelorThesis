import tensorflow as tf
import os
import cv2
import numpy as np
import datetime
from typing import List, Optional
from app.sparse_tensor_from_sequences import sparse_tensor_from_sequences
from app.vocabulary import VOCABULARY
from app.Dataset import Dataset


class Network:
    """
    In goes a grayscale image normalized to 0.0 - 1.0
    and out goes a sequence of classes (int[]).

    Number of classes is specified by a constructor parameter.
    Image height is a constant determined by the architecture.
    """

    IMAGE_HEIGHT = 64  # fixed by the CNN block architecture
    IMAGE_PADDING_COLOR = 0.0  # color to put after image end in a batch tensor
    NETWORK_SCOPE = "network"

    def __init__(
            self,
            name: str = None,
            vocabulary: Optional[List[str]] = None,
            continual_saving: bool = False,
            create_logdir: bool = False,
            threads: int = 1,
    ):
        # name of the model (for continual saving)
        self.name: str = name
        if self.name is None:
            raise Exception("Network name has to be specified")

        # vocabulary used for output encoding
        self.vocabulary: List[str] = VOCABULARY if vocabulary is None else vocabulary

        # number of output classes
        self.num_classes: int = len(self.vocabulary)

        # does the network save itself on improvement during dev evaluation?
        self.continual_saving: bool = continual_saving

        # whether summaries are logged or not
        self._has_summaries: bool = create_logdir

        # Create an empty graph and a session
        self.graph = tf.Graph()
        self.session = tf.Session(
            graph=self.graph,
            config=tf.ConfigProto(
                inter_op_parallelism_threads=threads,
                intra_op_parallelism_threads=threads
            )
        )

        # List fields that will be initialized during network construction
        self.images = None
        self.image_widths = None
        self.labels = None
        self.is_training = None
        self.learning_rate = None

        self.training = None
        self.reset_metrics = None
        self.saver = None

        # Construct the network
        logdir = None
        if create_logdir:
            logdir = Network.create_logdir(self.name)
        self.construct(logdir=logdir)

    ################################
    # Network structure definition #
    ################################

    def construct(self, logdir=None):
        """
        Constructs the computation TF graf.
        Needs to be called before anything is done with the network
        (right after the constructor).
        """
        with self.session.graph.as_default():

            # === input part ===

            # dataset data input
            self.images = tf.placeholder(
                tf.float32,
                [None, Network.IMAGE_HEIGHT, None],
                name="images"
            )
            self.image_widths = tf.placeholder(
                tf.int32,
                [None],
                name="widths"
            )
            self.labels = tf.sparse_placeholder(
                tf.int32,
                name="labels"
            )

            # metadata input
            self.is_training = tf.placeholder(
                tf.bool, [], name="is_training"
            )
            self.learning_rate = tf.placeholder(
                tf.float32, [], name="learning_rate"
            )

            # === trainable part ===

            with tf.variable_scope(Network.NETWORK_SCOPE):
                # CNN
                cnn_out_4d, widths = self._construct_cnn(
                    self.images,
                    self.image_widths
                )

                # RNN
                logits = self._construct_rnn(cnn_out_4d)

            # CTC
            losses = self._construct_ctc(
                logits,
                self.labels,
                widths
            )

            # === training logic part ===

            self.training = self._construct_training(
                self.learning_rate,
                self.loss
            )

            # === summaries, metrics and others part ===

            self._construct_metrics(losses, logdir)

            self.reset_metrics = tf.variables_initializer(
                tf.get_collection(tf.GraphKeys.METRIC_VARIABLES)
            )

            # Initialize variables
            self.session.run(tf.global_variables_initializer())

            # Saver
            self.saver = tf.train.Saver(
                var_list=tf.get_collection(
                    tf.GraphKeys.GLOBAL_VARIABLES,
                    #scope=Network.NETWORK_SCOPE # nope, save it with global_step
                )
            )

    def _construct_cnn(self, cnn_in_3d, widths):
        """Creates CNN layers and returns output of these layers"""
        cnn_in_4d = tf.expand_dims(input=cnn_in_3d, axis=3)

        # list of parameters for the layers
        kernel_vals = [5, 5, 5, 3, 3, 3]
        feature_vals = [1, 16, 32, 64, 128, 128, 256]
        stride_vals = pool_vals = [(2, 2), (2, 2), (2, 1), (2, 1), (2, 1), (2, 1)]
        num_layers = len(stride_vals)

        # create layers
        pool = cnn_in_4d # input to the first CNN layer
        for i in range(num_layers):
            kernel = tf.Variable(
                tf.truncated_normal(
                    [
                        kernel_vals[i],
                        kernel_vals[i],
                        feature_vals[i],
                        feature_vals[i + 1]
                    ],
                    stddev=0.1
                )
            )
            conv = tf.nn.conv2d(
                pool,
                kernel,
                padding="SAME",
                strides=(1, 1, 1, 1)
            )

            # TODO: possible batch normalization here

            relu = tf.nn.relu(conv)
            pool = tf.nn.max_pool(
                relu,
                (1, pool_vals[i][0], pool_vals[i][1], 1),
                (1, stride_vals[i][0], stride_vals[i][1], 1),
                "VALID"
            )

            # update widths of the images
            # (for RNN layers and CTC to know how wide is meaningful data)
            if pool_vals[i][1] == 2:
                widths = tf.floor_div(widths, tf.fill(tf.shape(widths), 2))

        return pool, widths

    def _construct_rnn(self, rnn_in_4d):
        """Creates RNN layers and returns output of these layers"""
        rnn_in_3d = tf.squeeze(rnn_in_4d, axis=[1])

        self.dropout = tf.placeholder(dtype=tf.float32, name="dropout")

        # basic cells which are used to build RNN
        num_hidden = 256
        num_layers = 1
        cells = [
            tf.nn.rnn_cell.DropoutWrapper(
                tf.contrib.rnn.LSTMCell(
                    num_units=num_hidden,
                    state_is_tuple=True
                ),
                input_keep_prob=1 - self.dropout
            )
            for _ in range(num_layers)
        ]

        # stack basic cells
        stacked = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        # bidirectional RNN
        # BxTxF -> BxTx2H
        ((fw, bw), _) = tf.nn.bidirectional_dynamic_rnn(
            cell_fw=stacked,
            cell_bw=stacked,
            inputs=rnn_in_3d,
            dtype=rnn_in_3d.dtype
        )

        fully_num_hidden = 256
        fully_layers = 0  # no fully connected layers after the RNN block

        # BxTxH + BxTxH -> BxTx2H
        rnn_outputs = tf.concat([fw, bw], 2)

        fully_hidden = rnn_outputs
        for _ in range(fully_layers):
            fully_hidden = tf.contrib.layers.fully_connected(
                fully_hidden,
                fully_num_hidden,
                activation_fn=None,
            )

        # reshape to output classes with a single fully connected layer
        return tf.contrib.layers.fully_connected(
            fully_hidden,
            self.num_classes + 1,
            activation_fn=None,
        )

    def _construct_ctc(self, logits, labels, logit_widths):
        """Creates the CTC loss and returns individual losses and their mean"""
        # time major
        logits = tf.transpose(logits, [1, 0, 2])

        # WARNING:
        # my version of tensorflow (1.12.0) uses "num_classes - 1" as the blank
        # index however the new tensorflow uses "0"
        if tf.__version__ not in ["1.12.0", "1.5.0"]:
            raise Exception("Make sure you know, how your blank is encoded!")

        # loss
        losses = tf.nn.ctc_loss(
            labels,
            logits,
            logit_widths
        )
        self.loss = tf.reduce_mean(losses)

        # beam predictions
        top_beam_predictions, _ = tf.nn.ctc_beam_search_decoder(
            logits,
            logit_widths,
            merge_repeated=False
        )
        self.predictions = top_beam_predictions[0]

        # greedy predictions
        top_greedy_predictions, _ = tf.nn.ctc_greedy_decoder(
            logits,
            logit_widths
        )
        self.greedy_predictions = top_greedy_predictions[0]

        # edit distance
        self.edit_distance = tf.reduce_mean(
            tf.edit_distance(
                self.predictions,
                tf.cast(labels, tf.int64)
            )
        )
        self.greedy_edit_distance = tf.reduce_mean(
            tf.edit_distance(
                self.greedy_predictions,
                tf.cast(labels, tf.int64)
            )
        )

        return losses

    def _construct_training(self, learning_rate, loss):
        """Creates an optimizer"""
        self.global_step = tf.train.create_global_step()
        return tf.train.AdamOptimizer().minimize(
            loss, global_step=self.global_step, name="training"
        )
        # return tf.train.RMSPropOptimizer(learning_rate).minimize(
        #     loss,
        #     global_step=self.global_step,
        #     name="training"
        # )

    def _construct_metrics(self, losses, logdir):
        """Creates summaries"""
        self.current_edit_distance, self.update_edit_distance = tf.metrics.mean(self.edit_distance)
        self.current_greedy_edit_distance, self.update_greedy_edit_distance = tf.metrics.mean(self.greedy_edit_distance)
        self.current_loss, self.update_loss = tf.metrics.mean(losses)

        # the following code handles logging
        # so continue only if we have a logdir specified
        if logdir is None:
            return

        summary_writer = tf.contrib.summary.create_file_writer(logdir, flush_millis=10 * 1000)

        self.summaries = {}

        with summary_writer.as_default(), tf.contrib.summary.record_summaries_every_n_global_steps(10):
            self.summaries["train"] = [
                tf.contrib.summary.scalar("train/loss", self.update_loss),
                tf.contrib.summary.scalar("train/edit_distance", self.update_greedy_edit_distance)
            ]

        with summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
            for dataset in ["dev", "test"]:
                self.summaries[dataset] = [
                    tf.contrib.summary.scalar(dataset + "/loss", self.current_loss),
                    tf.contrib.summary.scalar(dataset + "/edit_distance", self.current_edit_distance)
                ]

        with summary_writer.as_default():
            tf.contrib.summary.initialize(
                session=self.session,
                graph=self.session.graph
            )

    ###################
    # Utility methods #
    ###################

    @staticmethod
    def create_logdir(model_name: str):
        if not os.path.exists("tf-logs"):
            os.mkdir("tf-logs")
        return "tf-logs/{}-{}".format(
            model_name,
            datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        )

    @staticmethod
    def normalize_image(img: np.ndarray):
        # fix up image format
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        if img.max(initial=0) > 1.0:
            img = img / 255

        # normalize height
        target = Network.IMAGE_HEIGHT
        ratio = target / img.shape[0]
        w = int(img.shape[1] * ratio)
        return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)

    def encode_model_output(self, annotation: str) -> List[int]:
        return [self.vocabulary.index(s) for s in annotation.split()]

    def decode_model_output(self, model_output: List[int]) -> str:
        return " ".join([self.vocabulary[i] for i in model_output])

    def get_next_batch_from(self, dataset: Dataset, batch_size: int):
        images, annotations = dataset.next_batch(batch_size)

        take = len(images)
        assert len(images) == len(annotations)

        # pull data from dataset and normalize
        norm_images = [Network.normalize_image(img) for img in images]
        labels = [self.encode_model_output(a) for a in annotations]

        # convert the data into tensors
        max_image_width = max([i.shape[1] for i in norm_images])
        image_tensor = np.empty(
            shape=(take, Network.IMAGE_HEIGHT, max_image_width),
            dtype=np.float32
        )
        image_widths = np.empty(shape=(take,), dtype=np.int32)
        for i in range(take):
            w = norm_images[i].shape[1]
            image_tensor[i, :, 0:w] = norm_images[i]
            image_tensor[i, :, w:] = Network.IMAGE_PADDING_COLOR
            image_widths[i] = w

        return (
            image_tensor,
            image_widths,
            labels
        )

    #########################
    # Training & prediction #
    #########################

    def train(self, train_dataset, dev_dataset, epochs, batch_size):
        """
        Train the model for given number of epochs over a given training dataset
        and evaluate after each epoch on a given testing dataset.
        """
        for epoch in range(epochs):
            self.train_epoch(
                train_dataset,
                dev_dataset,
                epoch + 1,
                epochs,
                batch_size
            )

    def train_epoch(self, train_dataset, dev_dataset, epoch, epochs, batch_size):
        batches = train_dataset.count_batches(batch_size)
        batch = 1
        train_dataset.prepare_epoch()

        while train_dataset.has_batch():
            images, widths, labels = self.get_next_batch_from(train_dataset, batch_size)
            rate = self._calculate_learning_rate(self.get_global_step())

            # vars to evaluate
            evaluate = [self.loss, self.greedy_edit_distance, self.training]
            if self._has_summaries:
                evaluate.append(self.summaries["train"])

            # train
            self.session.run(self.reset_metrics)
            evaluated = self.session.run(evaluate, {
                self.images: images,
                self.image_widths: widths,
                self.labels: sparse_tensor_from_sequences(labels),
                self.is_training: True,
                self.learning_rate: rate,
                self.dropout: 0.5
            })

            loss = evaluated[0]
            greedy_edit_distance = evaluated[1]

            print("Epoch: %d/%s Batch: %d/%d Loss: %f ED: %f" % (
                epoch, str(epochs), batch, batches, loss, greedy_edit_distance
            ))

            batch += 1

        # and evaluate the performance after the epoch
        return self._evaluate(dev_dataset, batch_size)

    def _evaluate(self, dataset, batch_size, dataset_name="dev"):
        batches = dataset.count_batches(batch_size)
        batch = 1

        self.session.run(self.reset_metrics)
        dataset.prepare_epoch()

        right_items = 0
        all_items = 0
        wrong_examples = []

        while dataset.has_batch():
            images, widths, labels = self.get_next_batch_from(dataset, batch_size)
            predictions, _, _ = self.session.run([
                self.predictions,
                self.update_edit_distance,
                self.update_loss
            ], {
                self.images: images,
                self.image_widths: widths,
                self.labels: sparse_tensor_from_sequences(labels),
                self.is_training: False,
                self.dropout: 0.0
            })

            all_items += batch_size
            offset = 0
            for i in range(len(labels)):
                indices = predictions.indices[predictions.indices[:, 0] == i, 1]
                l = 0 if len(indices) == 0 else indices.max() + 1
                label: List[int] = labels[i]
                pred: List[int] = list(predictions.values[offset:offset+l])
                ok = "[ok]" if label == pred else "[err]"
                if label == pred:
                    right_items += 1
                print(
                    ok,
                    self.decode_model_output(label),
                    " ==> ",
                    self.decode_model_output(pred)
                )
                offset += l
                if label != pred:
                    wrong_examples.append((label, pred))

            print("Batch: %d / %d" % (batch, batches))

            batch += 1

        word_accuracy = (right_items / all_items) * 100
        edit_distance, loss = self.session.run([
            self.current_edit_distance,
            self.current_loss
        ])
        print("Edit distance: %f Word accuracy: %f%% Loss: %f" % (edit_distance, word_accuracy, loss))

        if word_accuracy >= 10: # do not show completely terrible results
            print("Some wrong examples:")
            for i in range(min(10, len(wrong_examples))):
                print(
                    self.decode_model_output(wrong_examples[i][0]),
                    " ==> ",
                    self.decode_model_output(wrong_examples[i][1])
                )

        # save validation loss and edit distance to summaries
        if self._has_summaries:
            self.session.run(self.summaries[dataset_name])

        # perform continual saving
        if self.continual_saving:
            self.save_if_better(edit_distance)

        # return loss and edit distance
        return loss, edit_distance

    def predict(self, img):
        """Predicts symbols in a single image"""
        img = Network.normalize_image(img)
        width = img.shape[1]

        predictions = self.session.run(self.predictions, {
            self.images: [img],
            self.image_widths: [width],
            self.is_training: False,
            self.dropout: 0.0
        })

        annotation: str = self.decode_model_output(predictions.values)

        return annotation

    def get_global_step(self):
        """Returns value of the global step"""
        return self.session.run(self.global_step)

    def _calculate_learning_rate(self, batches_trained):
        # return 0.01
        if batches_trained > 10000:
            return 0.0001
        elif batches_trained > 10:
            return 0.001
        else:
            return 0.01

    #####################
    # Model persistence #
    #####################

    """
        Models are persisted in the following files:
        - trained-models/{model-name}/model.index
        - trained-models/{model-name}/model.meta
        - trained-models/{model-name}/model.data-...
        - trained-models/{model-name}/checkpoint
        - trained-models/{model-name}/model.edit-distance
        - trained-models/{model-name}/model.vocabulary
    """

    @staticmethod
    def load(name: str, **kwargs):
        """Loads the model of a given name"""
        if not Network._exists(name):
            raise Exception("Model %s does not exist" % (name,))

        vocabulary = Network._load_vocabulary(name)
        network = Network(
            name=name,
            vocabulary=vocabulary,
            **kwargs
        )
        network.saver.restore(
            network.session,
            network._get_model_path(network.name)
        )

        return network

    def save(self, edit_distance=None):
        """Saves the model and also saves edit distance if provided"""
        dirname = self._get_model_directory(self.name)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        self.saver.save(
            self.session,
            self._get_model_path(self.name)
        )

        if edit_distance is not None:
            self._save_edit_distance(self.name, edit_distance)

        self._save_vocabulary(self.name)

    def _save_edit_distance(self, model_name: str, edit_distance: float):
        """Saves the edit distance"""
        dirname = self._get_model_directory(model_name)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        with open(self._get_model_path(model_name) + ".edit_distance", "w") as file:
            file.write(str(edit_distance))

    def _save_vocabulary(self, model_name: str):
        dirname = self._get_model_directory(model_name)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        with open(self._get_model_path(model_name) + ".vocabulary", "w") as file:
            file.write(str("\n".join(self.vocabulary)))

    def save_if_better(self, edit_distance):
        """Saves the model only if it has smaller edit distance, than the saved"""
        if self._get_saved_edit_distance(self.name) > edit_distance:
            print("Saving...")
            self.save(edit_distance)

    def _get_saved_edit_distance(self, model_name: str) -> float:
        """Returns edit distance of the saved model"""
        if not self._exists(model_name):
            return float("inf")

        with open(self._get_model_path(model_name) + ".edit_distance", "r") as file:
            ed = float(file.read())
        return ed

    @staticmethod
    def _load_vocabulary(model_name: str) -> List[str]:
        with open(Network._get_model_path(model_name) + ".vocabulary", "r") as file:
            return [l.strip() for l in file.readlines()]

    @staticmethod
    def _exists(model_name: str) -> bool:
        """Returns true if a given model exists"""
        return os.path.isdir(Network._get_model_directory(model_name))

    @staticmethod
    def _get_model_directory(model_name: str) -> str:
        """Returns directory path of a given model name"""
        return os.path.dirname(os.path.realpath(__file__)) + \
            "/../trained-models/" + model_name

    @staticmethod
    def _get_model_path(model_name: str) -> str:
        """Returns path for tensorflow saver to save the model to"""
        return Network._get_model_directory(model_name) + "/model"
