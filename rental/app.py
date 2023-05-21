import customtkinter as ctk

from pathlib import Path
from functools import partial
from typing import Callable

from tkinter import messagebox
from cassandra.cluster import NoHostAvailable

from . import util, stress
from .cassio import CassandraHandler
from .ui import UI, LoadingBox
from .data import models, mock
from .task import LongRunningTask
from .timer import Timer


class RentalApp:
    def __init__(self, cassandra_spec: dict):
        self.root = ctk.CTk()
        self.root.title("Rental App")
        self.sync_table = {}
        self.cass_spec = cassandra_spec

        self.ui = UI(self.root, model_names=[model.__name__ for model in models.MODELS])
        self.mock_data_dir = None
        self.cassandra_handler = CassandraHandler(**cassandra_spec)

        self.setup_button_callbacks()

        self.loading_box = LoadingBox()
        self.loading_box.after(100, self.initialize_connection)
        self.loading_box.mainloop()
        self.loading_box.destroy()

        def scheduled_table_sync():
            self.update_labels_from_sync_table()
            self.root.after(200, scheduled_table_sync)

        self.reload_model_counts()
        scheduled_table_sync()

    def reload_model_counts(self):
        for model in models.MODELS:
            tag = f"{util.name_to_tag(model.__name__)}_count"
            self.sync_table[tag] = str(model.objects.count())

    def on_clear_database(self):
        self.cassandra_handler.clear_tables(models.MODELS, safe=False)

    def on_repopulate_database(self):
        if self.mock_data_dir is None:
            raise ValueError("Mock data directory not set")
        if not self.mock_data_dir.exists():
            raise ValueError("Mock data directory does not exist")
        self.cassandra_handler.clear_tables(models.MODELS, safe=False)
        mock.load_mock_data(self.mock_data_dir)

    def set_mock_data_dir(self, mock_data_dir: Path):
        self.mock_data_dir = mock_data_dir

    def run(self):
        self.root.mainloop()

    def update_labels_from_sync_table(self):
        sync_copy = self.sync_table.copy()
        for key, value in sync_copy.items():
            self.ui.set_label_text(key, str(value))
        self.root.update()

    def setup_button_callbacks(self):
        self.register_long_action(self.on_clear_database, "clear_database", "DB Clear")
        self.register_long_action(
            self.on_repopulate_database, "repopulate_database", "DB Repopulate"
        )

        def same_request_test_wrapper():
            stress.same_request_test(requests_count=100)
            return {"successful_processes": "1/1"}

        self.register_long_action(
            same_request_test_wrapper,
            "stress_test_1",
            "Same Request Test [1]",
        )
        self.register_long_action(
            partial(util.run_concurrent_stress_test, stress_test_nr=2),
            "stress_test_2",
            "Random Actions Test [2]",
        )
        self.register_long_action(
            partial(util.run_concurrent_stress_test, stress_test_nr=3),
            "stress_test_3",
            "Random Actions Test [3]",
        )
        self.register_long_action(
            partial(util.run_concurrent_stress_test, stress_test_nr=4, num_clients=4),
            "stress_test_4",
            "Random Actions Test [4]",
        )

    def initialize_connection(self):
        try:
            self.cassandra_handler.setup(
                models.MODELS,
                lambda progress, status: self.loading_box.set_progress(
                    progress / 100, status
                )
                or self.loading_box.update(),
            )
        except NoHostAvailable:
            messagebox.showerror(
                "Connection Error",
                "Could not connect to Cassandra. Please check your connection settings.",
            )
            self.loading_box.quit()
            exit(1)
        self.loading_box.quit()

    def register_long_action(self, action: Callable, btn_tag: str, name: str) -> None:
        def on_start():
            for btn in self.ui.component_registry.button_registry.values():
                btn.configure(state="disabled")
            self.sync_table["status_value"] = f"Running {name}..."

        def on_complete():
            self.reload_model_counts()
            for btn in self.ui.component_registry.button_registry.values():
                btn.configure(state="normal")
            self.sync_table["status_value"] = "Idle"

        def timer_wrapped_action():
            with Timer() as timer:
                action_result = action()
            self.sync_table["time_value"] = f"{timer.elapsed():.2f}s"
            if action_result is not None:
                for key, value in action_result.items():
                    self.sync_table[key] = value

        self.ui.add_btn_command(
            btn_tag,
            lambda: LongRunningTask(
                timer_wrapped_action, on_start, on_complete
            ).start(),
        )
