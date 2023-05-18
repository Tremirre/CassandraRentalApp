import threading
from typing import Callable


class LongRunningTask:
    def __init__(
        self,
        task: Callable,
        on_start: Callable = lambda: None,
        on_complete: Callable = lambda: None,
        *args,
        **kwargs
    ) -> None:
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.on_complete = on_complete
        self.on_start = on_start
        self.thread = threading.Thread(target=self.run)

    def run(self) -> None:
        print("Starting task")
        self.task(*self.args, **self.kwargs)
        print("Task complete")
        self.on_complete()

    def start(self) -> None:
        self.on_start()
        self.thread.start()
