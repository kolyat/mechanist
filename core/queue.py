import persistqueue

from . import misc


class Queue:
    def __init__(self, name: str):
        self.queue = persistqueue.Queue(
            misc.get_tmp_path(name), tempdir=misc.get_tmp_path(),
            autosave=True
        )

    def put(self):
        self.queue.put(1)

    def get(self):
        try:
            self.queue.get(timeout=2)
        except persistqueue.Empty:
            pass

    def is_empty(self) -> bool:
        return True if self.queue.qsize() == 0 else False
