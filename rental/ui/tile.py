import customtkinter as ctk

from .registry import ComponentRegistry


class Tile(ctk.CTkFrame):
    def __init__(
        self, *args, title: str, component_registry: ComponentRegistry, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            width=200,
            font=("Roboto", 20),
        )
        self.title_label.pack(fill="x", padx=5, pady=5)
        self.content_grid = ctk.CTkFrame(self)
        self.content_grid.pack(fill="both", expand=True)
