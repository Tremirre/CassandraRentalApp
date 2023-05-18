import customtkinter as ctk

from pathlib import Path

from . import util

from .cassio import CassandraHandler
from .ui import UI
from .data import models, mock


class RentalApp:
    def __init__(self, cassandra_spec: dict):
        self.root = ctk.CTk()
        self.ui = UI(self.root, model_names=[model.__name__ for model in models.MODELS])
        self.mock_data_dir = None
        self.cassandra_handler = CassandraHandler(**cassandra_spec)
        self.cassandra_handler.setup(models.MODELS)

        self.ui.add_btn_command(
            "clear_database",
            self.on_clear_database,
        )

        self.ui.add_btn_command(
            "repopulate_database",
            self.on_repopulate_database,
        )
        self.reload_model_counts()

    def reload_model_counts(self):
        for model in models.MODELS:
            self.ui.set_label_text(
                f"{util.name_to_tag(model.__name__)}_count",
                str(model.objects.count()),
            )

    def on_clear_database(self):
        self.cassandra_handler.clear_tables(models.MODELS)
        self.reload_model_counts()

    def on_repopulate_database(self):
        if self.mock_data_dir is None:
            raise ValueError("Mock data directory not set")
        if not self.mock_data_dir.exists():
            raise ValueError("Mock data directory does not exist")
        self.cassandra_handler.clear_tables(models.MODELS)
        mock.load_mock_data(self.mock_data_dir)
        self.reload_model_counts()

    def set_mock_data_dir(self, mock_data_dir: Path):
        self.mock_data_dir = mock_data_dir

    def run(self):
        self.root.mainloop()
