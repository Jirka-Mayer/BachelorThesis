import tensorflow as tf
import os
import cv2
import datetime
from typing import List
from app.sparse_tensor_from_sequences import sparse_tensor_from_sequences
from app.vocabulary import decode_annotation_list


class Network:
    """
    In goes a grayscale image normalized to 0.0 - 1.0
    and out goes a sequence of classes (int[]).

    Number of classes is specified by a constructor parameter.
    Image height is a constant determined by the architecture.
    """

    IMAGE_HEIGHT = 64  # fixed by the CNN block architecture
    NETWORK_SCOPE = "network"

    def __init__(self, continual_saving=False, name=None, threads=1, num_classes=None):
        # name of the model (for continual saving)
        self.name = name

        # number of output classes
        self.num_classes: int = num_classes
        if self.num_classes is None:
            raise Exception("Number of output classes need to be specified")

        # does the network save itself on improvement during dev evaluation?
        self.continual_saving = continual_saving

        # whether summaries are logged or not
        self._has_summaries = False

        # Create an empty graph and a session
        self.graph = tf.Graph()
        self.session = tf.Session(
            graph=self.graph,
            config=tf.ConfigProto(
                inter_op_parallelism_threads=threads,
                intra_op_parallelism_threads=threads
            )
        )

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

            if logdir is not None:
                self._construct_summaries(losses, logdir)
                self._has_summaries = True

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
        stride_vals = pool_vals = [(2,2), (2,2), (2,1), (2,1), (2,1), (2,1)]
        numLayers = len(stride_vals)

        # create layers
        pool = cnn_in_4d # input to the first CNN layer
        for i in range(numLayers):
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
                strides=(1,1,1,1)
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
        if tf.__version__ != "1.12.0":
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

    def _construct_summaries(self, losses, logdir):
        """Creates summaries"""
        self.current_edit_distance, self.update_edit_distance = tf.metrics.mean(self.edit_distance)
        self.current_greedy_edit_distance, self.update_greedy_edit_distance = tf.metrics.mean(self.greedy_edit_distance)
        self.current_loss, self.update_loss = tf.metrics.mean(losses)

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

    @staticmethod
    def create_logdir(model_name: str):
        if not os.path.exists("tf-logs"):
            os.mkdir("tf-logs")
        return "tf-logs/{}-{}".format(
            model_name,
            datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
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
            images, labels, widths = train_dataset.next_batch(batch_size)
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
            images, labels, widths = dataset.next_batch(batch_size)
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
                    decode_annotation_list(label),
                    " ==> ",
                    decode_annotation_list(pred)
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
                    decode_annotation_list(wrong_examples[i][0]),
                    " ==> ",
                    decode_annotation_list(wrong_examples[i][1])
                )

        # save validation loss and edit distance to summaries
        if self._has_summaries:
            self.session.run(self.summaries[dataset_name])

        # perform continual saving
        if self.continual_saving:
            self.save_if_better(self.name, edit_distance)

        # return loss and edit distance
        return loss, edit_distance

    def predict(self, img):
        """Predicts symbols in a single image"""
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        if img.max() > 1.0:
            img = img / 255

        width = img.shape[1]
        assert img.shape[0] == Network.IMAGE_HEIGHT

        predictions = self.session.run(self.predictions, {
            self.images: [img],
            self.image_widths: [width],
            self.is_training: False,
            self.dropout: 0.0
        })

        return predictions.values

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

    # TODO: continue here
