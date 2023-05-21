import customtkinter as ctk

from ..util import name_to_tag
from .registry import ComponentRegistry


class SideFrame(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        component_registry: ComponentRegistry,
        width=200,
        app_title: str = "RentApp",
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(fill="y", side="left", ipadx=10, ipady=10)
        self.app_title_label = ctk.CTkLabel(
            self,
            text=app_title,
            width=width,
            font=("Roboto", 32),
        )
        self.app_title_label.pack(fill="x", padx=10, pady=10)
        for text in ("Admin", "User", "Testing"):
            button = component_registry.make_button(
                name_to_tag(text),
                self,
                text=text,
                width=width,
                font=("Roboto", 16),
            )
            button.pack(fill="x", padx=10, pady=10)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=10, pady=10, anchor="s")

        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)

        self.time_label = ctk.CTkLabel(
            self.stats_frame,
            text="Task Time: ",
            font=("Roboto", 12),
        )
        self.time_label.grid(row=0, column=0, sticky="w", padx=10)

        self.time_value_label = component_registry.make_label(
            "time_value",
            self.stats_frame,
            text="0.0s",
            font=("Roboto", 12),
        )
        self.time_value_label.grid(row=0, column=1, sticky="e", padx=10)

        self.status_label = ctk.CTkLabel(
            self.stats_frame,
            text="Status: ",
            font=("Roboto", 12),
        )
        self.status_label.grid(row=1, column=0, sticky="w", padx=10)

        self.status_value_label = component_registry.make_label(
            "status_value",
            self.stats_frame,
            text="Idle",
            font=("Roboto", 12),
        )
        self.status_value_label.grid(row=1, column=1, sticky="e", padx=10)
