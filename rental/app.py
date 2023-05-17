import customtkinter as ctk

from .cassio import CassandraHandler
from .ui import UI
from .data import models


class RentalApp:
    def __init__(self, cassandra_spec: dict):
        self.root = ctk.CTk()
        self.ui = UI(self.root)
        self.cassandra_handler = CassandraHandler(**cassandra_spec)
        self.cassandra_handler.setup(models.MODELS)

        self.ui.add_btn_command(
            "clear_database",
            self.on_clear_database,
        )

    def on_clear_database(self):
        self.cassandra_handler.teardown()
        self.cassandra_handler.setup(models.MODELS)

    def run(self):
        self.root.mainloop()
