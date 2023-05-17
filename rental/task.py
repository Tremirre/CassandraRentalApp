import threading
from typing import Callable


class LongRunningTask:
    def __init__(self, task: Callable, on_complete: Callable, *args, **kwargs) -> None:
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.on_complete = on_complete

        self.thread = threading.Thread(target=self.run)

    def run(self) -> None:
        self.task(*self.args, **self.kwargs)
        self.on_complete()

    def start(self) -> None:
        self.thread.start()
