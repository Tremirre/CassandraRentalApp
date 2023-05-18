import customtkinter as ctk

from pathlib import Path

from tkinter import messagebox
from cassandra.cluster import NoHostAvailable

from . import util
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

        scheduled_table_sync()

    def reload_model_counts(self):
        for model in models.MODELS:
            tag = f"{util.name_to_tag(model.__name__)}_count"
            self.sync_table[tag] = str(model.objects.count())

    def on_clear_database(self):
        with Timer() as timer:
            self.cassandra_handler.clear_tables(models.MODELS, safe=False)
            self.reload_model_counts()
        self.sync_table["time_value"] = f"{timer.elapsed():.2f}s"

    def on_repopulate_database(self):
        with Timer() as timer:
            if self.mock_data_dir is None:
                raise ValueError("Mock data directory not set")
            if not self.mock_data_dir.exists():
                raise ValueError("Mock data directory does not exist")
            self.cassandra_handler.clear_tables(models.MODELS, safe=False)
            mock.load_mock_data(self.mock_data_dir)
            self.reload_model_counts()

        self.sync_table["time_value"] = f"{timer.elapsed():.2f}s"

    def set_mock_data_dir(self, mock_data_dir: Path):
        self.mock_data_dir = mock_data_dir

    def run(self):
        self.root.mainloop()

    def update_labels_from_sync_table(self):
        for key, value in self.sync_table.items():
            self.ui.set_label_text(key, str(value))
        self.sync_table.clear()
        self.root.update()

    def setup_button_callbacks(self):
        self.ui.add_btn_command(
            "clear_database",
            lambda: LongRunningTask(self.on_clear_database).start(),
        )

        self.ui.add_btn_command(
            "repopulate_database",
            lambda: LongRunningTask(self.on_repopulate_database).start(),
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
