import numpy as np
from app.Dataset import Dataset
from app.AnnotationsDataset import AnnotationsDataset
from threading import Thread
from queue import Queue


PRINT_DEBUG_INFO = False


class ParallelFeedingDataset(Dataset):
    def __init__(self, source: Dataset, queue_size=100):
        super().__init__()

        # the source dataset that contains the actual data
        self.source = source

        # swap out the get_image method
        self.original_source_get_image = self.source.get_image
        self.source.get_image = self.get_image_source_replacement

        # copy of self.permutation
        self._indices_to_prepare: np.ndarray = None

        # preparing thread
        self._worker_thread: Thread = None

        # queue of prepared images
        self._queue = Queue(
            maxsize=queue_size  # buffer only so many images
                                # to keep the memory overhead constant
        )

    ######################################
    # Redirect API to the source dataset #
    ######################################

    def check_dataset_visually(self, example_count=10):
        if isinstance(self.source, AnnotationsDataset):
            self.source.get_image = self.original_source_get_image
            self.source.check_dataset_visually(example_count)
            self.source.get_image = self.get_image_source_replacement
        else:
            raise Exception("Source dataset does not allow inspection")

    @property
    def size(self) -> int:
        return self.source.size

    def get_annotation(self, index: int) -> str:
        return self.source.get_annotation(index)

    def has_batch(self):
        return self.source.has_batch()

    def count_batches(self, batch_size):
        return self.source.count_batches(batch_size)

    ######################################################
    # Hook into important methods and not quite redirect #
    ######################################################

    def prepare_epoch(self):
        self.source.prepare_epoch()

        self._indices_to_prepare = self.source.permutation.copy()
        self._worker_thread = Thread(
            target=self._worker_thread_loop,
            daemon=True
        )
        self._worker_thread.start()

    def next_batch(self, batch_size=1):
        batch = self.source.next_batch(batch_size)

        if not self.source.has_batch():
            self._last_batch_prepared()

        return batch

    ######################################################
    # Replacement for the get_image method of the source #
    ######################################################

    def get_image_source_replacement(self, index: int) -> np.ndarray:
        if self._worker_thread is None:
            raise Exception("prepare_epoch() hasn't been called")

        given_img, given_index = self._queue.get(
            block=True  # wait for an item
        )
        assert given_index == index
        return given_img

    #######################
    # Worker thread logic #
    #######################

    def _worker_thread_loop(self):
        if PRINT_DEBUG_INFO:
            print("[worker] Started.")

        n = len(self._indices_to_prepare)
        for i in range(n):
            index = self._indices_to_prepare[i]
            if PRINT_DEBUG_INFO:
                print("[worker] Preparing item " + str(i))

            img = self.original_source_get_image(index)
            self._queue.put(
                (img, index),
                block=True  # wait for a free slot (when queue full)
            )

        if PRINT_DEBUG_INFO:
            print("[worker] Done.")

    def _last_batch_prepared(self):
        if PRINT_DEBUG_INFO:
            print("Joining on the worker...")

        self._worker_thread.join()

        if PRINT_DEBUG_INFO:
            print("Worker joined.")
